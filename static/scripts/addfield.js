document.addEventListener("DOMContentLoaded", function (){
    let div = document.getElementById("id_block-w-ingr");
    let numd = 1;
    document.getElementById("id_addbtn-newingr").addEventListener("click", () => {
        let newInput = document.createElement("input");
        newInput.placeholder = "Название";
        newInput.name = "ingrName" + numd;
        newInput.type = "text";
        let newInputD = document.createElement("input");
        newInputD.placeholder = "Описание";
        newInputD.name = "ingrDesc" + numd;
        newInputD.type = "text";
        let newContainer = document.createElement("div");
        newContainer.className = "block_ingredients_container";

        let deleteBtn = document.createElement("button");
        deleteBtn.type = "button";
        deleteBtn.className = "block_ingredients_delbtn"
        deleteBtn.innerHTML = "Убрать ингредиент";
        div.appendChild(newContainer);
        newContainer.appendChild(newInput);
        newContainer.appendChild(newInputD);
        newContainer.appendChild(deleteBtn);
        numd++;
        deleteBtn.onclick = function (e ){
            this.parentNode.parentNode.removeChild(this.parentNode);
            numd--;
        }

    });

    let steps = document.getElementById("id_block-w-steps");
    let i = 0;

    document.getElementById("id_addbtn-step-text").addEventListener("click", ()=>{
        let newContainerT = document.createElement("div");
        newContainerT.className = "step_card-text";

        let stepcounter = document.createElement("p");
        stepcounter.className = "step_card-counter";
        stepcounter.innerHTML = "Шаг "+ ++i;

        let inputField = document.createElement("textarea");
        inputField.name = "descriptionStep" + i;
        inputField.className = "step_card-description";
        inputField.required = true;
        newContainerT.appendChild(stepcounter);
        newContainerT.appendChild(inputField);

        steps.appendChild(newContainerT);
    });

    document.getElementById("id_addbtn-step-img").addEventListener("click", ()=>{
        let newContainerI = document.createElement("div");
        newContainerI.className = "step_card-img";

        let stepcounter = document.createElement("p");
        let cont = document.createElement("div");
        cont.className = "step_card-info";
        stepcounter.className = "step_card-counter";
        stepcounter.innerHTML = "Шаг "+ ++i;

        let inputField = document.createElement("textarea");
        inputField.name = "descriptionStep" + i;
        inputField.className = "step_card-description";
        inputField.required = true;
        let label = document.createElement("label");
        let inputFileI = document.createElement("input");
        inputFileI.name = "cardimage" + i;
        let img = document.createElement("img");
        img.src = "/static/img/icon-addimage.svg";
        inputFileI.type = "file";
        label.appendChild(inputFileI);
        label.appendChild(img);

        cont.appendChild(stepcounter);
        cont.appendChild(inputField);
        newContainerI.appendChild(cont);
        newContainerI.appendChild(label);

        inputFileI.addEventListener('change', function (e) {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function (event) {
                    label.style.backgroundImage = "url(" + event.target.result +")";
                };
                reader.readAsDataURL(file);
            }
        })

        steps.appendChild(newContainerI);
    });
});
