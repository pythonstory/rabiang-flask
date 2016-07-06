YUI().use(
    'aui-dropdown',
    'aui-carousel',
    function (Y) {
        var navbarToggle = Y.one(".navbar-toggle");
        var navbarCollapse = Y.one(".navbar-collapse");

        navbarToggle.on('click', function (e) {
            if (navbarCollapse.hasClass("in")) {
                navbarCollapse.removeClass("in");
                navbarCollapse.setStyle("height", "0px");
            } else {
                navbarCollapse.addClass("in");
                navbarCollapse.setStyle("height", "auto");
            }
        });

        Y.all('.dropdown').each(
            function (node) {
                new Y.Dropdown({
                    boundingBox: node,
                    trigger: node.one('.dropdown-toggle')
                }).render();
            });
    }
);