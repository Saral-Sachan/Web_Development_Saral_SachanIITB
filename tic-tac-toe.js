let btn = document.querySelectorAll(".btn");
let resetbtn=document.querySelector(".resetbtn");
let winner=document.querySelector(".winner");
let turn0 = true; //first player     
btn.forEach((btn) => {
    btn.addEventListener("click", () => {
        if (turn0) {
            btn.innerText = "O";
            btn.style.color = "blue";
            btn.style.borderColor="blue";
            turn0 = false;
        }
        else {
            btn.innerText = "X";
            btn.style.color = "red";
            btn.style.borderColor="red";
            turn0 = true;
        }
        btn.disabled = true; //ensuring one btn can be clicked only once
        checkWinner();
    })

})
const winning_patterns = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
];
const disableBtns=()=>{
    btn.forEach((butn)=>{
        butn.disabled= true;
    })
}
const enableBtns=()=>{
    btn.forEach((butn)=>{
        butn.disabled= false;
    })
}
const resetGame=()=>{
    turn0= true;
    enableBtns();
    winner.classList.add("hide");
    btn.forEach((btns)=>{
        btns.innerText="";
        btns.style.borderColor="black";
    })
}
resetbtn.addEventListener("click",resetGame);


const checkWinner =()=>{
    for(let pattern of winning_patterns){
        let pos1val = btn[pattern[0]].innerText;
        let pos2val = btn[pattern[1]].innerText;
        let pos3val = btn[pattern[2]].innerText;

        if(pos1val !="" && pos2val!="" && pos3val!=""){
            if(pos1val === pos2val && pos2val === pos3val){
                console.log(`Winner ${pos1val}`);
                winner.innerText=`Winner: ${pos1val}`;
                disableBtns();
                winner.classList.remove("hide");

            }
        }

    }
}




