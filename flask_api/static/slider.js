var sliderAmountMap = [2011, 2013, 2016, 2021, 2026, 2031, 2036, 2041];
 
$(function() {
    $( "#slider" ).slider({
        value: 0, // Initial value
        min: 0, // Min slider length
        max: sliderAmountMap.length-1, // Max slider length
        slide: function( event, ui ) {
            $( "#year" ).text( sliderAmountMap[ui.value] );
            loadDoc( sliderAmountMap[ui.value].toString() ); 
        }
    });
});