function hi(text) {
    console.log(text);
};

function select_all() {
  let inputs = document.getElementsByTagName('input');
  for (let i = 0;i<inputs.length;i++){
    inputs[i].checked = true;
  }
};