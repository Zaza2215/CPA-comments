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
