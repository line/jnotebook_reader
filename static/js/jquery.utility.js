(function (factory) {
    if (typeof define === "function" && define.amd) {
        // AMD
        define("jquery.utility", ["jquery"], factory);
    } else if (typeof exports === "object") {
        // CommonJS
        factory(require("jquery"));
    } else {
        // Browser globals
        factory(jQuery);
    }
}(function ($) {

    $.copyToClipboard = function (text) {
        var textarea = $("<textarea></textarea>");
        textarea.text(text);
        $("body").append(textarea);
        textarea.on("focus", function () {
            $(this).select();
            document.execCommand("copy");
            $(this).remove();
        });
        textarea.focus();
    };
}));