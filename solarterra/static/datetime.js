function dtw_initTimeContainer(prefix) {

    // creating time seconds
    let secondsScroll = document.getElementById(`${prefix}-seconds-scroll`);
    let secondsTemplate = document.getElementById(`${prefix}-second-template`);

    for (let i = 0; i < 60; i++) {
        
        let value = i < 10 ? `0${i}` : `${i}`;
    
        let newOption = secondsTemplate.cloneNode(true);
        newOption.innerHTML = value;
        secondsScroll.append(newOption);
        newOption.id = `${prefix}-second-${value}`;

    }

    // creating time minutes
    let minutesScroll = document.getElementById(`${prefix}-minutes-scroll`);
    let minutesTemplate = document.getElementById(`${prefix}-minute-template`);

    for (let i = 0; i < 60; i++) {

        let value = i < 10 ? `0${i}` : `${i}`;

        let newOption = minutesTemplate.cloneNode(true);
        newOption.innerHTML = value;
        minutesScroll.append(newOption);
        newOption.id = `${prefix}-minute-${value}`;
    }

    // creating time hours
    let hoursScroll = document.getElementById(`${prefix}-hours-scroll`);
    let hoursTemplate = document.getElementById(`${prefix}-hour-template`);

    for (let i = 0; i < 24; i++) {

        let value = i < 10 ? `0${i}` : `${i}`;

        let newOption = hoursTemplate.cloneNode(true);
        newOption.innerHTML = value;
        hoursScroll.append(newOption);
        newOption.id = `${prefix}-hour-${value}`;
    }

}

function dtw_initInput(inputId) {
    
    let el = document.getElementById(inputId);

    
    if (el.hasAttribute('data-sub')) {
        
        dtw_launchRerender(el);
        let savedDate = new Date( Date.parse(el.dataset.sub));

        let hh = String(savedDate.getHours()).padStart(2, '0');
        let mm = String(savedDate.getMinutes()).padStart(2, '0');
        let ss = String(savedDate.getSeconds()).padStart(2, '0');
        document.getElementById(`${el.dataset.prefix}-hour-${hh}`).click();
        document.getElementById(`${el.dataset.prefix}-minute-${mm}`).click();
        document.getElementById(`${el.dataset.prefix}-second-${ss}`).click();

        let month = String(savedDate.getMonth() + 1).padStart(2, '0');
        let day = String(savedDate.getDate()).padStart(2, '0');
        document.getElementById(`${el.dataset.prefix}-day-${day}-${month}`).click();
    } else {
        console.log("initial not found");

        let now = new Date();
        el.dataset.months = String(now.getMonth() + 1).padStart(2, '0');
        el.dataset.days = String(now.getDate()).padStart(2, '0');
        el.dataset.year = String(now.getFullYear()).padStart(2, '0');
        
    }

    
}

//
var DTW_MONTHS_LIST = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"]

var WEEK_DAYS = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]

function dtw_initCalendarContainer(prefix) {


    /* fill in week day names */

    let weekdaysContainer = document.getElementById(`${prefix}-cal-weekdays`);
    let weekdayTemplate = document.getElementById(`${prefix}-cal-weekday-template`);

    for (let i = 0; i < WEEK_DAYS.length; i++) {
        let wday = weekdayTemplate.cloneNode(true);
        wday.id = null;
        wday.innerHTML = WEEK_DAYS[i];
        weekdaysContainer.append(wday);
    }

    dtw_renderCalNav(prefix, new Date());
    dtw_renderCalDays(prefix);
    dtw_renderCalMonths(prefix);
    dtw_renderCalYears(prefix);
}



function dtw_renderCalNav(prefix, someDate=null) {
    let prevMonthLabel = document.getElementById(`${prefix}-prev-month-label`);
    let nextMonthLabel = document.getElementById(`${prefix}-next-month-label`);
    let currentMonthLabel = document.getElementById(`${prefix}-current-month-label`);
    let currentYearLabel = document.getElementById(`${prefix}-current-year-label`);
    
    let firstDate = new Date(someDate.getFullYear(), someDate.getMonth(), 1);
    let lastDate = null;
    if (someDate.getMonth() == 11) {
        lastDate = new Date(someDate.getFullYear() + 1, 0, 0);
    } else {
        lastDate = new Date(someDate.getFullYear(), someDate.getMonth() + 1, 0);
    }
        
    let oneDayInMs = 24 * 60 * 60 * 1000;

    // here we need to change previous and next month dates (first day of the month - 1);
    let prevMonthDate = new Date(firstDate.getTime() - oneDayInMs);
    let nextMonthDate = new Date(lastDate.getTime() + oneDayInMs);
   

    prev_mm = String(prevMonthDate.getMonth() + 1).padStart(2, '0');
    next_mm = String(nextMonthDate.getMonth() +  1).padStart(2, '0');
    dd = String(someDate.getDate()).padStart(2, '0');

    
    prevMonthLabel.dataset.sub = `${prevMonthDate.getFullYear()}-${ prev_mm }-${dd}`;
    nextMonthLabel.dataset.sub = `${nextMonthDate.getFullYear()}-${ next_mm }-${dd}`;
    currentMonthLabel.innerHTML = DTW_MONTHS_LIST[someDate.getMonth()];
    currentYearLabel.innerHTML = someDate.getFullYear();
}

function dtw_renderCalYears(prefix, someDate=null) {

    let currentDate = (someDate !== null) ? someDate : new Date();
    console.log("render calyears", currentDate);

    /* generate year choices */
    let yearTemplate = document.getElementById(`${prefix}-year-choice-template`);
    let yearsTemplate = document.getElementById(`${prefix}-years-choice-template`);
    let yearsContainer = document.getElementById(`${prefix}-cal-years-container`);

    yearsContainer.innerHTML = '';

    let mm = String(currentDate.getMonth() + 1).padStart(2, '0');
    console.log("MONTHS", mm);
    let yearLine = null;
    for (let i = 0; i < 150; i++) {
        if (i % 4 == 0) {
            yearLine = yearsTemplate.cloneNode(true);
            yearLine.id = null;
            yearsContainer.append(yearLine);
            
        }
        let yearElement = yearTemplate.cloneNode(true);
        yearElement.id = null;
        yearElement.dataset.sub = `${1950 + i}-${mm}-01`;
        yearElement.innerHTML = 1950 + i;
        yearLine.append(yearElement);
    }

}


function dtw_renderCalMonths(prefix, someDate=null) {

    let currentDate = (someDate !== null) ? someDate : new Date();
    console.log("render calmonths", currentDate);
    /* generate month choices */
    let monthTemplate = document.getElementById(`${prefix}-month-choice-template`);
    let monthsTemplate = document.getElementById(`${prefix}-months-choice-template`);
    let monthsContainer = document.getElementById(`${prefix}-cal-months-container`);

    monthsContainer.innerHTML = '';

    let monthLine = null;
    for (let i = 0; i < 12; i++) {
        if (i % 3 == 0) {
            monthLine = monthsTemplate.cloneNode(true);
            monthLine.id = null;
            monthsContainer.append(monthLine);
            
        }
        
        let monthElement = monthTemplate.cloneNode(true);
        monthElement.id = null;
        mm = String(i + 1).padStart(2, '0');
        monthElement.dataset.sub = `${currentDate.getFullYear()}-${mm}-01`;
        monthElement.innerHTML = DTW_MONTHS_LIST[i];
        monthLine.append(monthElement);
    }
}

function dtw_renderCalDays(prefix, someDate=null, highlight=true) {

    let currentDate = (someDate !== null) ? someDate : new Date();
    let firstDate = new Date(currentDate.getFullYear(), currentDate.getMonth(), 1);
    let lastDate = new Date(currentDate.getFullYear(), currentDate.getMonth() + 1, 0);
    
    let oneDayInMs = 24 * 60 * 60 * 1000;
    
    // first render day
    let firstDateWeekDay = firstDate.getDay();
    let diff = (firstDateWeekDay - 1);
    diff = (diff < 0) ? 6 : diff;
    let diffInMs = oneDayInMs * diff;
    let firstRenderDay = new Date( firstDate - diffInMs);

    // last render day
    let lastDateWeekDay = lastDate.getDay();
    lastDateWeekDay = (lastDateWeekDay == 0) ? lastDateWeekDay : 7 - lastDateWeekDay;
    let diflInMs = oneDayInMs * lastDateWeekDay;
    let lastRenderDay = new Date( lastDate.getTime() + diflInMs );

    
    let actualCal = document.getElementById(`${prefix}-cal-days-container`);
    let calDayEl = document.getElementById(`${prefix}-cal-day-template`);
    let calWeek = document.getElementById(`${prefix}-cal-week-container-template`);


    let iterDate = firstRenderDay;
    let i = 0;
    let classMonth = currentDate.getMonth();

    while (iterDate <= lastRenderDay) {          
                
        if (i % 7 == 0) {
            daysLine = calWeek.cloneNode(true);
            daysLine.id = null;
            actualCal.append(daysLine);
        }

        mm = String(iterDate.getMonth() + 1).padStart(2, '0');
        dd = String(iterDate.getDate()).padStart(2, '0');

        let dayElement = calDayEl.cloneNode(true);
        dayElement.id = `${prefix}-day-${dd}-${mm}`;
        dayElement.innerHTML = iterDate.getDate();
        

        dayElement.dataset.sub = `${iterDate.getFullYear()}-${mm}-${dd}`;
        daysLine.append(dayElement);
        
        if (iterDate.getMonth() !== classMonth) {
            dayElement.classList.add('dtw-cal-inactive');
        }

        if (highlight && iterDate.getDate() == currentDate.getDate() && iterDate.getMonth() == currentDate.getMonth()) {
            dayElement.classList.add('dtw-cal-selected');
        }

        iterDate = new Date (iterDate.getTime() + oneDayInMs);
        
        i++;
        
    }  
}

function dtw_launchRerender(element, hide_months=false, hide_years=false) {

    console.log(element);

    let prefix = element.dataset.prefix;

    let actualCalDays = document.getElementById(`${prefix}-cal-days-container`);
    actualCalDays.innerHTML = "";
    
    let newDate = new Date( Date.parse(element.dataset.sub));
    
    highlight = !(hide_months || hide_years)

    dtw_renderCalDays(prefix, newDate, highlight);
    dtw_renderCalMonths(prefix, newDate);
    dtw_renderCalYears(prefix, newDate);
    dtw_renderCalNav(prefix, newDate);

    
    if (hide_months === true) {
        console.log("hiding months");
        let hideTarget = document.getElementById(`${prefix}-current-month-label`);
        pairVisibility(hideTarget);

    }
    
    if (hide_years === true) {
        console.log("hiding years");
        let hideTarget = document.getElementById(`${prefix}-current-year-label`);
        pairVisibility(hideTarget);
    }
    
}


function changeVisibility(element) {
    
    if (typeof element === "string") {

            element = document.getElementById(element);
    }
    if (element) {
            
            element.hidden = !(element.hidden);
    } else {
            console.log("In changeVisibility: element not found");
    }
}


function pairVisibility(element) {

    let first = element.dataset.first;
    let second = element.dataset.second;
    let third = document.getElementById(element.dataset.third);

    console.log(third);

    if (third.hidden) {
        changeVisibility(first);
        changeVisibility(second);
    } else {
        changeVisibility(third);
        changeVisibility(first);
    }
}


function removeClassFromClass(container, groupClass, targetClass) {
    let collection = container.getElementsByClassName(groupClass);
    console.log("collection", collection.length)
    for (let i = 0; i < collection.length; i++) {
        collection[i].classList.remove(targetClass);
    }
}

function dtw_chooseTimeOption(element) {
    element.scrollIntoView({ behavior: "smooth"});
    let targetEl = document.getElementById(element.dataset.target);
    prefix = targetEl.id;
    elementContainer = document.getElementById(`${prefix}-datetime-container`);

    if (element.id.startsWith(`${prefix}-hour`)) {
        targetEl.dataset.hours = element.innerText;
        removeClassFromClass(elementContainer, "dtw-js-hours", "dtw-time-option-selected");
    }
    if (element.id.startsWith(`${prefix}-minute`)) {
        targetEl.dataset.minutes = element.innerText;
        removeClassFromClass(elementContainer, "dtw-js-minutes", "dtw-time-option-selected");
    }
    if (element.id.startsWith(`${prefix}-second`)) {
        targetEl.dataset.seconds = element.innerText;
        removeClassFromClass(elementContainer, "dtw-js-seconds", "dtw-time-option-selected");
    }

    dtw_buttonExchange(prefix, false);
    
    document.getElementById(`${prefix}-hour-${targetEl.dataset.hours}`).classList.add("dtw-time-option-selected");
    document.getElementById(`${prefix}-minute-${targetEl.dataset.minutes}`).classList.add("dtw-time-option-selected");
    document.getElementById(`${prefix}-second-${targetEl.dataset.seconds}`).classList.add("dtw-time-option-selected");
       
    targetEl.value = `${targetEl.dataset.year}-${targetEl.dataset.months}-${targetEl.dataset.days} ${targetEl.dataset.hours}:${targetEl.dataset.minutes}:${targetEl.dataset.seconds}`;
  
    confButtonChange(prefix, true);
}

function dtw_chooseDateOption(element) {
    
    let targetEl = document.getElementById(element.dataset.target);

    console.log(targetEl);

    
    targetEl.dataset.year = element.dataset.sub.substring(0,4);
    targetEl.dataset.months = element.dataset.sub.substring(5,7);
    targetEl.dataset.days = element.dataset.sub.substring(8,10);


    dtw_buttonExchange(targetEl.id, false);

    targetEl.value = `${targetEl.dataset.year}-${targetEl.dataset.months}-${targetEl.dataset.days} ${targetEl.dataset.hours}:${targetEl.dataset.minutes}:${targetEl.dataset.seconds}`;
  
    dtw_launchRerender(element);
    confButtonChange(targetEl.id, true);
}


function show(element) {
    if (typeof element === "string") {
            element = document.getElementById(element);
    }
    if (element) {
            element.hidden = false;  
    } else {
            console.log("In changeVisibility: element not found");
    }
}

function hide(element) {
    if (typeof element === "string") {
            element = document.getElementById(element);
    }
               
    if (element) {
            element.hidden = true;
    } else {
            console.log("In changeVisibility: element not found");
    }
}


function confButtonChange(prefix, change) {
    let but = document.getElementById(`${prefix}-confirm-button`);

    if (change) {
        but.classList.remove("dtw-cb-inactive");
        but.classList.add("dtw-cb-active");
    } else {
        but.classList.remove("dtw-cb-active");
        but.classList.add("dtw-cb-inactive");
    }
}

function dtw_buttonExchange(prefix, clear) {
    let clearTimeButton = document.getElementById(`${prefix}-clear-datetime`);
    let chooseTimeButton = document.getElementById(`${prefix}-choose-datetime`);

    if (clear) {
        show(chooseTimeButton);
        hide(clearTimeButton);
    } else {
        hide(chooseTimeButton);
        show(clearTimeButton);
    }
}


function dtw_clearInput(clearEl, element_id) {    
    let targetEl = document.getElementById(element_id);
    targetEl.value = '';
    targetEl.dataset.hours = '00';

    elementContainer = document.getElementById(`${prefix}-datetime-container`);
    removeClassFromClass(elementContainer, "dtw-js-hours", "dtw-time-option-selected");
    targetEl.dataset.minutes = '00';
    removeClassFromClass(elementContainer, "dtw-js-minutes", "dtw-time-option-selected");
    targetEl.dataset.seconds = '00';
    removeClassFromClass(elementContainer, "dtw-js-seconds", "dtw-time-option-selected");
    
    dtw_buttonExchange(element_id, true);
    confButtonChange(element_id, false);
    
    document.getElementById('hour-00').scrollIntoView({ behavior: "smooth"});
    document.getElementById('minute-00').scrollIntoView({ behavior: "smooth"});
    document.getElementById('second-00').scrollIntoView({ behavior: "smooth"});        
}
