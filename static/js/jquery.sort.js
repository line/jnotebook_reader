(function (factory) {
    if (typeof define === "function" && define.amd) {
        // AMD
        define("jquery.sort", ["jquery"], factory);
    } else if (typeof exports === "object") {
        // CommonJS
        factory(require("jquery"));
    } else {
        // Browser globals
        factory(jQuery);
    }
}(function ($) {

    $.fn.sortable = function () {
        var tpl = `
            <a href="javascript:void(0)" class="sort">
                <span></span>
                <i class="fas fa-2x fa-fw fa-sort" sortable></i>
                <i class="fas fa-2x fa-fw fa-sort-down" down></i>
                <i class="fas fa-2x fa-fw fa-sort-up" up></i>
            </a>
        `;

        var tbl = $(this);
        $.each(tbl.find("thead th"), function (i, value) {
            var text = $(value).text();
            if ($(value)[0].hasAttribute("sortable") && text.length > 0) {
                var sort = $(tpl);
                sort.find("span").text(text);
                $(value).html("");
                $(value).append(sort);
            }
        });
        tbl.find("thead a.sort").on("click", function () {
            var self = $(this);
            var index = self.closest("th").index();
            var rows = tbl.find("tbody tr").toArray();
            rows.sort(function (r1, r2) {
                var v1 = $.trim($(r1).find("td").eq(index).attr("sort-by"));
                var v2 = $.trim($(r2).find("td").eq(index).attr("sort-by"));
                if (self.find("i[down]").is(":hidden")) {
                    if (!isNaN(v1) && !isNaN(v2)) {
                        return v2 - v1;
                    }
                    return v2.localeCompare(v1);
                } else {
                    if (!isNaN(v1) && !isNaN(v2)) {
                        return v1 - v2;
                    }
                    return v1.localeCompare(v2);
                }
            });
            rows.forEach(function (row) {
                $("tbody").append($(row));
            });
            if (self.find("i[down]").is(":hidden")) {
                tbl.find("i.fa-fw").hide();
                self.find("i[up]").hide();
                self.find("i[down]").show();
            } else {
                tbl.find("i.fa-fw").hide();
                self.find("i[up]").show();
                self.find("i[down]").hide();
            }
        });
    }
}));