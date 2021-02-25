let quantity = document.getElementById('quantity')
console.log(quantity)
function increment(){
    quantity.value++
}

function decrement(){
    if (quantity.value != 0){
    quantity.value --
    }
}