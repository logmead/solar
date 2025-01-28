/*
 *      Plugin date & time
 *      ------------------
 *
 *      Manage datetime from input text
 *      display date and time singly
 */

(function($) {

	$.fn.dateAndTime = function() {

		let elementMain = $(this);
		console.log(elementMain);

		// for each element, evalute date and time to split
		elementMain.each(function(index, ele) { 

			let element = $(ele);

			// check attribute class exits only
			if (element.attr('class') === undefined || element.attr('class').length === 0) {
				console.error('dateAndTime : You must have an attribute class to use this !');
				return false;
			}

			let class_name       = element.attr('class');
			let date             = element.val().split(' ')[0];
			let time             = element.val().split(' ')[1] || '00:00'; 
			let css_class_custom = class_name;

			// check the node type text
			if (element.attr('type') !== 'text') {
				console.error('js_datetime : You must have an attribute text to use this !');
				return false;
			}

			// remove class added on the main input hidden
			if (css_class_custom.length > 0)
				element.removeClass(css_class_custom);

			// put content raw html and fill classes added on the new inputs
			// on elements jQuery
			let eleDateTime = $(`
			<input type="date" value="${date}" class="${css_class_custom}">
			<input type="time" value="${time}" class="${css_class_custom}">
			`);

			// add inputs and attr done to flag
			element
				.before(eleDateTime)
				.attr('done', true)
				.hide();

			// put event into the loop
			$(eleDateTime, $(element).not('[done="true"]')).change(function(e) {
				let currentDateTime = $(e.currentTarget),	
				      selectElement = element;

				// set inputs hidden field
				currentDateTime.attr('value', currentDateTime.val());				
				if (currentDateTime.attr('type') === 'date') {		
					date = currentDateTime.val();			
					time = '00:00';
				} else { 
					time = currentDateTime.val();
				}
				// set values on inputs
				selectElement.attr('value', date + ' ' + time);

				return false;

			}); 

		});

	}


} (jQuery));

