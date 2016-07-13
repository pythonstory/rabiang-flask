tinymce.init({
    selector: '#post_body',
    height: 400,
    theme: 'modern',
    plugins: [
        'advlist autolink lists link image charmap print preview hr anchor pagebreak',
        'searchreplace wordcount visualblocks visualchars code fullscreen',
        'insertdatetime media nonbreaking save table contextmenu directionality',
        'emoticons template paste textcolor colorpicker textpattern imagetools'
    ],
    toolbar1: 'undo redo | styleselect | bold italic forecolor backcolor fontselect | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | link image media emoticons | print preview',
    image_advtab: true,
    /*
    templates: [
        { title: 'Test template 1', content: 'Test 1' },
        { title: 'Test template 2', content: 'Test 2' }
    ],
    */
    content_css: [
        '//fonts.googleapis.com/css?family=Lato:300,300i,400,400i',
        '//www.tinymce.com/css/codepen.min.css'
    ],
    relative_urls: false,
    remove_script_host : false,
    convert_urls : true,
    file_browser_callback: function(field_name, url, type, win) {
        if (type == 'image') {
            // Open file browser
            document.getElementById('photo').click();

            // hidden field in order to pass the popup field name
            document.getElementById('field_name').value = field_name;
        }
    },
});

function ajax_upload(element) {
    // Retrieve field_name from hidden field.
    var field_name = document.getElementById('field_name').value;

    var formData = new FormData(document.getElementById('upload_image_form'));

    // ajax upload
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function(e){
        if (xhr.readyState == 4 && xhr.status == 200) {
            document.getElementById(field_name).value = xhr.responseText;
        }
    }
    xhr.open('POST', '/page/ajax-upload-image/', false);
    xhr.send(formData);
}
