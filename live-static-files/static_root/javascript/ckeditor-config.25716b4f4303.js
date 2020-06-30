CKEDITOR.editorConfig = function( config ) {

    var options = {
        toolbar: [
            ['Format', 'Bold', 'Italic', 'Underline', 'Strikethrough', '-', 'Subscript', 'Superscript', '-', 'TextColor'],
            ['JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock'],
            ['NumberedList', 'BulletedList', '-', 'Blockquote'],
            ['Link', 'Unlink'],
            ['Table', '-', 'Image'],
            ['ShowBlocks', 'Source']
        ],
        toolbarCanCollapse: true,
        format_tags: 'p;h2;h3;h4;h5',
        coreStyles_strike: {element: 'del', overrides: 'strike'},
        coreStyles_underline: {element: 'ins', overrides: 'u'},
        scayt_autoStartup: false,
        disableNativeSpellChecker: false,
        filebrowserUploadUrl: '/ckeditor/upload/',
        filebrowserBrowseUrl: '/ckeditor/browse/'
    };

    $.extend(config, options);

};
