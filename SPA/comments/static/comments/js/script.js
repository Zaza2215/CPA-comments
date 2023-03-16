 const textarea = document.getElementById('id_body');
 const button_a = document.getElementById('btn-tag-a');
 const button_i = document.getElementById('btn-tag-i');
 const button_s = document.getElementById('btn-tag-strong');
 const button_c = document.getElementById('btn-tag-code');


button_a.onclick = function() {
    textarea.value += '<a href="" title=""></a>';
  };
button_i.onclick = function() {
    textarea.value += '<i></i>';
  };
button_s.onclick = function() {
    textarea.value += '<strong></strong>';
  };
button_c.onclick = function() {
    textarea.value += '<code></code>';
  };


const imageUploader = document.getElementById('id_image');

imageUploader.addEventListener('change', () => {
  const file = imageUploader.files[0];
  const allowedExtensions = /(\.jpg|\.jpeg|\.png|\.gif)$/i;
  if (!allowedExtensions.exec(file.name)) {
    alert('Ошибка! Разрешены только файлы с расширениями .jpg, .png и .gif.');
    imageUploader.value = '';
    return false;
  }
});

const fileInput = document.getElementById('id_file');

fileInput.addEventListener('change', (event) => {
  const file = event.target.files[0];

  if (file && file.type === 'text/plain' && file.size <= 100 * 1024) {
    // файл удовлетворяет условиям
    console.log(`Файл ${file.name} был успешно загружен.`);
    // здесь можно выполнить отправку файла на сервер или другие операции с ним
  } else {
    // файл не удовлетворяет условиям
    alert('Пожалуйста, выберите файл с расширением .txt и размером не более 100 Кб.');
    // очистим input file, чтобы пользователь мог выбрать другой файл
    fileInput.value = '';
  }
});