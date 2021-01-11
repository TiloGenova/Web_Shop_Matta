console.log('TO2')

var updateBtns = document.getElementsByClassName('update-cart')

for (var i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click',function(){
        var productId = this.dataset.product
        var action = this.dataset.action
        console.log('productId:',productId, 'action:', action)

        //var db=openDatabase("db.sqlite3","1.0", "db.sqlite3", 65535);


        console.log('USER:', user)
        if(user === 'AnonymousUser'){
            addCookieItem(productId, action)
        }else{
            updateUserOrder(productId, action)
        }
   })

}

function addCookieItem(productId, action){
    console.log('Not logged in..')

    if(action == 'add'){
        if(cart[productId] == undefined){
            cart[productId] = {'quantity':1}
        }else{
            cart[productId]['quantity'] += 1
        }

    }

    if(action == 'remove'){
        cart[productId]['quantity'] -= 1

        if(cart[productId]['quantity'] <= 0){
            console.log('Remove item')
            delete cart[productId]
        }
    }

    console.log('Cart:', cart)
    document.cookie = 'cart='+JSON.stringify(cart) + ";domain=;path=/"
    location.reload()

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
