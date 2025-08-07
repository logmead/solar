from django.core.management.base import BaseCommand, CommandError, CommandParser
# from load_cdf.models import dataset, datasetAttribute, datasetAttributeValue,\
# Variable, VariableAttribute, VariableAttributeValue
from load_cdf.models import dataset, datasetAttribute, datasetAttributeValue, \
    Variable, VariableAttribute, VariableAttributeValue, VariableDataNRV, make_log_entry
import datetime as dt
from spacepy import pycdf
import os
from solarterra.utils import normalize_str
import random


"""
list of file attributes
list of variable names with a list of attributes

"""


MATCH_DELIM = "%"


class Load():

    # note: i am pretty sure that "xattr" and other things starting with "x" are related to the former naming of Dataset, Experiment
    # i am lazy to rename it

    def __init__(self, dir_path, file_count, dataset_technical):

        self.dataset = Dataset(
            dir_path=dir_path,
            technical_title=dataset_technical,
            file_count=file_count)

        self.dset_attrs = []

        self.dset_attr_values = []

        self.vars = []

        self.var_attrs = []

        self.var_attr_values = []

        self.nrv_data = []

    def l_dset_attr(self, m):
        return (m, m.title)

    def l_dset_attr_val(self, m):
        return (m, f"{m.attribute.id}{MATCH_DELIM}{m.value}")

    def l_var(self, m):
        return (m, m.name)

    def l_var_attr(self, m):
        return (m, f"{m.variable.id}{MATCH_DELIM}{m.title}{MATCH_DELIM}{m.data_type}")

    def l_var_attr_val(self, m):
        return (m, f"{m.attribute.id}{MATCH_DELIM}{m.value}")

    def abstract_search(self, match_string, l_func, array):

        filtered = filter(lambda n: n[1] == match_string, map(l_func, array))
        match = next(filtered, None)

        if match is not None:
            return match[0]
        else:
            return None

    def len_dset_attrs(self):
        return len(self.dset_attrs)

    # def dset_attrs_stats(self):
    #     for attr in self.dset_attrs:
    #         print(f"attr *{attr.title}* values {attr.unique_values}")

    # def var_stats(self):
    #     for var in self.vars:
    #         print(f"var *{var.name}*")

    def add_dset_attr_val(self, **kwargs):
        """
        sending here a value and an dset_attr instance
        looking for a saved value
        """

        if 'new' not in kwargs:
            match_string = f"{kwargs['xattr_instance'].id}{MATCH_DELIM}{kwargs['value']}"
            attrval = self.abstract_search(
                match_string, self.l_dset_attr_val, self.dset_attr_values)
            if attrval is not None:
                return False

        xattrval = DatasetAttributeValue(
            value=kwargs['value'],
            attribute=kwargs['xattr_instance'],
        )

        self.dset_attr_values.append(xattrval)

        return True

    def add_dset_attr(self, **kwargs):
        """
        looking for this attribute in saves:l
        """
        match_string = kwargs['title']
        attr = self.abstract_search(
            match_string, self.l_dset_attr, self.dset_attrs)

        if attr is not None:
            new_value = self.add_dset_attr_val(
                xattr_instance=attr, value=kwargs['value'])
            if new_value:
                attr.unique_values += 1
            return

        # did not find it, add it and its values
        xattr = DatasetAttribute(
            dataset=self.dataset,
            title=kwargs['title'],
            unique_values=1,
            unique_for_file=False,
        )

        self.dset_attrs.append(xattr)
        self.add_dset_attr_val(
            new=True, xattr_instance=xattr, value=kwargs['value'])

    def set_unique_attr_values(self):
        for attr in self.dset_attrs:
            if attr.unique_values == self.dataset.file_count:
                attr.unique_for_file = True

    def add_vars(self, **kwargs):

        match_string = kwargs['name']
        var = self.abstract_search(match_string, self.l_var, self.vars)
        if var is not None:
            return var

        var = Variable(
            dataset=self.dataset,
            name=kwargs['name'],
            data_type=kwargs['data_type'],
            shape=kwargs['shape'],
            non_record_variant=kwargs['nrv'],
        )

        self.vars.append(var)
        return var

    def add_var_attr_val(self, **kwargs):
        """
        sending here a value and an var_attr instance
        looking for a saved value
        """
        if 'new' not in kwargs:
            match_string = f"{kwargs['var_attr_instance'].id}{MATCH_DELIM}{kwargs['value']}"
            vattrval = self.abstract_search(
                match_string, self.l_var_attr_val, self.var_attr_values)

            if vattrval is not None:
                return False

        vattrval = VariableAttributeValue(
            value=kwargs['value'],
            attribute=kwargs['var_attr_instance'],
        )
        self.var_attr_values.append(vattrval)

        return True

    def add_var_attr(self, **kwargs):
        """
        looking for this var attribute in saves:
        """

        match_string = f"{kwargs['variable'].id}{MATCH_DELIM}{kwargs['title']}{MATCH_DELIM}{kwargs['data_type']}"
        attr = self.abstract_search(
            match_string, self.l_var_attr, self.var_attrs)

        if attr is not None:
            new_value = self.add_var_attr_val(
                var_attr_instance=attr, value=kwargs['value'])
            if new_value:
                attr.unique_values += 1
            return  # ugh a funny mechanic for interrupting procedure execution

        # did not find it, add it and its values
        vattr = VariableAttribute(
            variable=kwargs['variable'],
            title=kwargs['title'],
            data_type=kwargs['data_type'],
            unique_values=1,
        )

        self.var_attrs.append(vattr)
        self.add_var_attr_val(
            new=True, var_attr_instance=vattr, value=kwargs['value'])

    def add_nrv_values(self, **kwargs):

        # did not make a check of existing here
        # ❓j: should we?

        nrv = VariableDataNRV(
            variable=kwargs['variable'],
            value=kwargs['value'],
            order=kwargs['order'],
        )

        self.nrv_data.append(nrv)


class Command(BaseCommand):
    def add_arguments(self, parser):
        # parser is a built-in BaseCommand class that takes command line arguments
        # narg is a number of arguments that can be passed to the command
        parser.add_argument("dir_path", nargs="+", type=str)
        # nargs can be a number, a + or a *, where + means one or more

    def handle(self, *args, **options):

        # what are the rest of the options? why is it a list? #a: the rest of the options are the additional directory paths that can be passed to the command. it is a list because nargs="+" allows for one or more arguments to be passed
        dir_path = options["dir_path"][0]
        make_log_entry(
            "START", f"Evaluation script launched with parameter \"{dir_path}\"")

        files_list = []
        for (dirpath, dirnames, filenames) in os.walk(dir_path):
            files_list.extend(
                [f"{dirpath}/{filename}" for filename in filenames if filename.endswith('.cdf')])

        file_number = len(files_list)

        path_parts = dir_path.split('/')

        dataset_technical = path_parts[-1] if path_parts[-1] != '' else path_parts[-2]

        make_log_entry("", "Checking for collisions...")

        second = Dataset.objects.get_or_none(technical_title=dataset_technical)
        if second is None:
            make_log_entry(
                "NOT FOUND", f"Existing Data Type with name \"{dataset_technical}\" not found")
        else:
            make_log_entry(
                "ERROR", f"Existing Data Type with name \"{dataset_technical}\" already found")
            make_log_entry("EXIT", "Evaluation script finished")
            exit(1)

        if file_number == 0:
            make_log_entry(
                "ERROR", f"Data Type \"{dataset_technical}\", in {dir_path} found {file_number} .cdf files")
            make_log_entry("EXIT", "Evaluation script finished")
            exit(1)
        else:
            make_log_entry(
                "FOUND", f"Data Type \"{dataset_technical}\", in {dir_path} found {file_number} .cdf files")

        load = Load(dir_path, file_number, dataset_technical)
        make_log_entry("", "Evaluating metadata...")

        # get everything from any one file

        # j: i bet json gets in there, this random one will be for validation purposes
        random_index = random.randint(0, len(files_list))

        cdf_obj = pycdf.CDF(files_list[random_index])

        for xkey, xvalue in cdf_obj.attrs.items():
            load.add_exp_attr(title=normalize_str(xkey),
                              value=str(xvalue).strip())

        for key in cdf_obj.keys():

            type_class = cdf_obj[key].dtype.__name__ if hasattr(
                cdf_obj[key].dtype, '__name__') else cdf_obj[key].dtype.__class__.__name__

            var_instance = load.add_vars(
                name=normalize_str(key),
                data_type=type_class,
                shape=str(cdf_obj[key].shape),
                nrv=not (cdf_obj[key].rv())
            )

            for attr_key, attr_value in cdf_obj[key].attrs.items():
                if attr_key == 'VAR_TYPE' and attr_value == 'data':
                    var_instance.is_data = True
                    # print(f"FOUND COMBO on {var_instance}")

                data_type = type(attr_value).__name__
                load.add_var_attr(variable=var_instance, title=normalize_str(
                    attr_key), data_type=data_type, value=str(attr_value).strip())

            if var_instance.non_record_variant:
                val_array = cdf_obj[key]
                for index, val in enumerate(val_array):
                    load.add_nrv_values(
                        variable=var_instance, value=val, order=index)

        make_log_entry("", "Saving metadata...")

        load.dataset.save()
        load.set_unique_attr_values()
        DatasetAttribute.objects.bulk_create(load.dset_attrs)
        DatasetAttributeValue.objects.bulk_create(load.dset_attr_values)
        Variable.objects.bulk_create(load.vars)
        VariableAttribute.objects.bulk_create(load.var_attrs)
        VariableAttributeValue.objects.bulk_create(load.var_attr_values)
        VariableDataNRV.objects.bulk_create(load.nrv_data)
        make_log_entry(
            "CREATED", f"Metadata for Data Type \"{dataset_technical}\" saved")
        make_log_entry("PREPROCESSING", "Evaluation stage compeleted")

        del cdf_obj
        del load
