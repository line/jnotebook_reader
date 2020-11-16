define([], function () {
    require.config({
        paths: {
            "jquery": "jquery-3.3.1",
            "jquery-ui": "jquery-ui",
            "bootstrap": "bootstrap.bundle-4.3.1",
            "nbextensions/toc2/toc2": "toc2"
        },
        shim: {
            "jquery-ui": ["jquery"],
        }
    });
});