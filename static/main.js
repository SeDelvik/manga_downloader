function hi(text) {
    console.log(text);
};

function select_all() {
    let funky_button = document.getElementById('funky_button');
    let inputs = document.getElementsByTagName('input');
    for (let i = 0;i<inputs.length;i++){
        inputs[i].checked = true;
    }
    funky_button.setAttribute("onClick","deselect_all()");
    funky_button.innerHTML = "Отменить";
};

function deselect_all(){
    let funky_button = document.getElementById('funky_button');
    let inputs = document.getElementsByTagName('input');
    for (let i = 0;i<inputs.length;i++){
        inputs[i].checked = false;
    }
    funky_button.setAttribute("onClick","select_all()");
    funky_button.innerHTML = "Выделить всё";
}