window.onload = function () {
    document.getElementById('id_image').addEventListener('change', function (e) {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function (event) {
                const preview = document.getElementById('preview');
                preview.src = event.target.result;
                preview.style.display = 'block';
            };
            reader.readAsDataURL(file);
            formsaver = document.getElementById('id_change_photo-form');
            if(formsaver){
                document.getElementById('id_changephoto-btn').style.display = "block"
            }
        }
    });

};