$(document).ready(function () {


    $(window).scroll(function () {
        if ($(document).scrollTop() >= 50) {
            $('.header-menu').addClass('navbar-fixed');
        } else {
            $('.header-menu').removeClass('navbar-fixed');
        }
    });



    // Check Width 
    function checkWidth() {
        var windowSize = $(window).width();
        if (windowSize <= 768) {
            var maxLength = 300;
            $(".show-read-more").each(function () {
                var myStr = $(this).text();
                if ($.trim(myStr).length > maxLength) {
                    var newStr = myStr.substring(0, maxLength);
                    var removedStr = myStr.substring(maxLength, $.trim(myStr).length);
                    $(this).empty().html(newStr);
                    $(this).append('<br/>');
                    $(this).append('<a href="javascript:void(0);" class="read-more">Read More</a>');
                    $(this).append('<span class="more-text">' + removedStr + '</span>');
                }
            });
            $(".read-more").click(function () {
                $(this).siblings(".more-text").contents().unwrap();
                $(this).remove();
            });
        }

    }
    // open
    $('.open').click(function () {
        $('.open').css("display", "none");
        $('.close').css("display", "block");
        $('.toggle-logo').css("color", "transparent");
        $('.toggle-logo').bind('click', false);
    });


    $('.close').click(function () {
        $('.open').css("display", "block");
        $('.close').css("display", "none");
        $('.toggle-logo').css("color", "#c94f9b");
        $('.toggle-logo').unbind('click', false);
    });
    //close

    // Check Width 
    checkWidth();
    activePageLinkControl();
});

function activePageLinkControl() {
    $('.pagination .page-item a').click(function () {
        $('.page-item').removeClass('active')
        $(this).closest('.page-item').addClass('active')
    })
}

function goBack() {
    window.history.back();
}


// number or not check//
function isNumberKey(evt) {
    var charCode = (evt.which) ? evt.which : evt.keyCode;
    if (charCode != 46 && charCode > 31 &&
        (charCode < 48 || charCode > 57))
        return false;

    return true;
}
// number or not check//