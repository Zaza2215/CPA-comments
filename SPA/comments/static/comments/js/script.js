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
    alert('Error! Only files with extensions .jpg, .png and .gif are allowed.');
    imageUploader.value = '';
    return false;
  }
});

const fileInput = document.getElementById('id_file');

fileInput.addEventListener('change', (event) => {
  const file = event.target.files[0];

  if (file && file.type === 'text/plain' && file.size <= 100 * 1024) {
    console.log(`Файл ${file.name} был успешно загружен.`);
  } else {
    alert('Please choose a file with .txt extension and no more than 100 Kb in size.');
    fileInput.value = '';
  }
});

const replyButtons = document.querySelectorAll('.button-reply');
  for (var i = 0; i < replyButtons.length; i++) {
    replyButtons[i].addEventListener('click', function() {
      const commentId = this.getAttribute('data-comment-id');
      document.getElementById('id_parent').value = commentId;
    });
}

const noReplyButton = document.getElementById("no-reply");
const parentInput = document.getElementById("id_parent");

noReplyButton.addEventListener("click", function() {
  parentInput.value = "";
});