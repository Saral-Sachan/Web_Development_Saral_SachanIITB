const BASE_URL =
  "https://cdn.jsdelivr.net/gh/fawazahmed0/currency-api@1/latest/currencies";

const dropdowns = document.querySelectorAll(".dropdown select");
const btn = document.querySelector("form button");
const fromCurr = document.querySelector(".from select");
const toCurr = document.querySelector(".to select");
const msg = document.querySelector(".result p");

// for (code in countryList){  // in-->access KEYs
//   console.log(code, countryList[code]);
// }

for(let select of dropdowns){ //select--to and from
  for(currCode in countryList){
    let newOption = document.createElement("option");
    newOption.innerText= currCode;
    newOption.value=currCode;
    if(select.name==="from" && currCode==="USD"){
      newOption.selected="selected";
    }
    else if(select.name==="to" && currCode==="INR"){
      newOption.selected="selected";
    }
    select.append(newOption);
  }
  select.addEventListener("change", (evt)=>{
    updateFlag(evt.target); //target returns the element where change happens
  })
}
const updateFlag=(element)=>{ //element is select
  let currCode = element.value;
  // console.log(currCode);
  let countryCode = countryList[currCode];
  let newSrc = `https://flagsapi.com/${countryCode}/flat/64.png`;
  let img = element.parentElement.querySelector("img");
  img.src = newSrc;

};

btn.addEventListener("click",async (evt)=>{
  evt.preventDefault(); //prevents auto behaviour like refreshing of forms
  let amount = document.querySelector(".amount input");
  let amtVal = amount.value;
  if(amtVal==="" || amtVal<1){
    amtVal = 1;
    amount.value = "1";
  }
  const URL = `${BASE_URL}/${fromCurr.value.toLowerCase()}/${toCurr.value.toLowerCase()}.json`;

  let response = await fetch(URL);
  let data = await response.json();
  let rate = data[toCurr.value.toLowerCase()];
  console.log(rate);
  let finalAmt = amtVal * rate;
  msg.innerText = finalAmt;

})
