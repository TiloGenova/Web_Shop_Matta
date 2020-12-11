console.log('TO2')

var updateBtns = document.getElementsByClassName('update-cart')

for (var i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click',function(){
        var productId = this.dataset.product
        var action = this.dataset.action
        console.log('productId:',productId, 'action:', action)

        console.log('USER:', user)
        if(user === 'AnonymousUser'){
        console.log('Not logged in')
        }else{
        updateUserOrder(productId, action)
        }
   })

}

function updateUserOrder(productId, action){
    console.log('User is authenticated, sending data...')

    var url = '/update_item/'  //

    fetch(url, {
        method: 'POST',    // POST to send data   POST -CSFR Token in Django needed
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken':csrftoken,
            },
            body: JSON.stringify({'productId':productId, 'action': action})   // the data, which is send to the backend
        })   // above all to send the data



        .then((response) => {
            return response.json();
        })
        .then((data) =>{
            console.log('data:', data)
            location.reload()    // reload the page
        });

}
