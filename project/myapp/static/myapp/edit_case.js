// when the page, edit_case.html is loaded, run this function
document.addEventListener("DOMContentLoaded", function() {

    //create variables that scan the document by class
    // these are all the toggles on the left side in edit_case.html
    const deceasedInfo = document.querySelector('.personal_info_toggle')
    const obituary = document.querySelector('.obituary_toggle')
    const events = document.querySelector('.events_toggle')
    const finances = document.querySelector('.finances_toggle')
    const complete = document.querySelector('.complete_toggle')
    
    // when we land on this page we are decided to display Deceased Info initially
    // so access styling here and only display deceased info
    deceasedInfo.style.display = "block"
    obituary.style.display = "none"
    events.style.display = "none"
    finances.style.display = "none"
    complete.style.display = "none"


    // create variable that gets my template in html (line - 310)
    // you made a template because you decided it was easier to recreate the html rather
    // than grabbing all the variable back here to javascript
    // this way, keeping everything in the template as a class, you can grab
    // everything from html easy, but your styling stays the same too
    const template = document.getElementById('product_template')

    // create variable that looks for the id=new_product in my HTML (line - 221)
    // this is the input field where user can select a product
    const productSelection = document.querySelector('#new_product')

    // create variable that gets the ID deceasedId, hidden in my HTML in my HTML (line - 267)
    // this ID is hidden in the finance page so we can keep track of the finances of that person
    const deceasedId = document.getElementById('deceasedId').textContent.trim()

    // when there is a CHANGE to the product selection... do this function
    productSelection.addEventListener("change", function(){

        // create a variable that stores the VALUE (value corrolates with INPUTS) of the input field, productSelection
        // this which product the user selected from the list
        const product = productSelection.value
        console.log(product)
        
        // start a fetch call to send the info to python
        // run the function 'save_finance' (views.py, line - 275) with the deceacedId we had hidden from before
        fetch(`/save_finance/${deceasedId}/`,{
        method: "POST",
        body:JSON.stringify({
            // the package that goes to python is on the left
            // we can call it anything, as long as you use the same name in python
            // product on the left is from above - line(33)
            product:product
        })
    })
        // after our fetch call, after the function runs in python
        // take the response
        .then(response => response.json())

        // store in information as RESULT
        .then(result => {

            // your WALL for your product variable is your product list in edit_case.html (line - 273)
            const productWall = document.getElementById("product_list")
            
            // takes the tempate from above that we got from html
            // grabs the content, whats inside the templete
            // .cloneNode(true), makes a copy of it, true - copy everything not just first element
            const clone = template.content.cloneNode(true)


            // of the COPY/clone we made, get whats inside the package
            // the NAME, CATEGORY, and PRICE
            // everything else is still in the clone, like the edit and delete, 
            // **just putting the right textContent in the right places**
            clone.querySelector(".product_name").textContent = result.name
            clone.querySelector(".product_category").textContent = result.category
            clone.querySelector(".product_quantity").textContent = result.quantity
            clone.querySelector(".product_quantity").id = `product_quantity_${result.id}`
            clone.querySelector(".product_price").id = `product_price_${result.id}`
            clone.querySelector(".product_price").textContent = `$${result.price.toFixed(2)}`
            clone.querySelector(".product_delete").href = `/delete_product/${result.id}` 
            clone.querySelector(".product_edit").id = `product_edit_${result.id}`
            clone.querySelector(".product_notes").textContent = result.notes
            clone.querySelector(".product_notes").id = `product_notes_${result.id}`
            clone.querySelector(".edit_product").id = `edit_product_${result.id}`
            clone.querySelector(".edit_notes").id = `edit_notes_${result.id}`
            clone.querySelector(".edit_quantity").id = `edit_quantity_${result.id}`
            clone.querySelector(".edit_price").id = `edit_price_${result.id}`
            clone.querySelector(".edit_button").id = `edit_button_${result.id}`
            clone.querySelector(".cancel_button").id = `cancel_button_${result.id}`


            if (result.notes == null) {
                clone.querySelector(".product_notes").style.display = "none"
            }
            else {
                clone.querySelector(".product_notes").style.display = "block"
            }
            
            clone.querySelector('.product_edit').setAttribute('onclick', `editProduct({
                                        id: ${result.id},
                                        name: "${result.name}", 
                                        category: "${result.category}",
                                        description: "${result.description}"})`)

            // take the clone and append it to the productWall aka your PRODUCT LIST
            // set the value of the input field to nothing so a new product can be selected
            
            selectedProduct = document.querySelector('#new_product')
            selectedProduct.value = ""
            productWall.append(clone)




            // NEED NOTES and QUantity LINE 322 in HTML
        
        


            // old total cost = the textContent on the h6 - total cost when the page is loaded
            // this is the total that is calculated when we land of the page
            // slice so we get rid of the 'Total: ' and only use the text. 
            const old_total_cost = document.getElementById("total_cost").textContent.slice(7)
            
            // old total cost + the 'newPrice' = new total cost
            const new_total_cost = parseFloat(old_total_cost) + parseFloat(result.price)


            document.querySelector("#total_cost").textContent = `Total: ${new_total_cost.toFixed(2)}`

            

    
        })
    })

});



function deceasedInfoClick(){
    const deceasedInfo = document.querySelector('.personal_info_toggle')
    const obituary = document.querySelector('.obituary_toggle')
    const events = document.querySelector('.events_toggle')
    const finances = document.querySelector('.finances_toggle')
    const complete = document.querySelector('.complete_toggle')
    deceasedInfo.style.display = "block"
    obituary.style.display = "none"
    events.style.display = "none"
    finances.style.display = "none"
    complete.style.display = "none"
}

function obituaryClick(){
    const deceasedInfo = document.querySelector('.personal_info_toggle')
    const obituary = document.querySelector('.obituary_toggle')
    const events = document.querySelector('.events_toggle')
    const finances = document.querySelector('.finances_toggle')
    const complete = document.querySelector('.complete_toggle')
    deceasedInfo.style.display = "none"
    obituary.style.display = "block"
    events.style.display = "none"
    finances.style.display = "none"  
    complete.style.display = "none"  
}

function eventsClick(){
    const deceasedInfo = document.querySelector('.personal_info_toggle')
    const obituary = document.querySelector('.obituary_toggle')
    const events = document.querySelector('.events_toggle')
    const finances = document.querySelector('.finances_toggle')
    const complete = document.querySelector('.complete_toggle')
    deceasedInfo.style.display = "none"
    obituary.style.display = "none"
    events.style.display = "block"
    finances.style.display = "none"   
    complete.style.display = "none" 
}

function financesClick(){
    const deceasedInfo = document.querySelector('.personal_info_toggle')
    const obituary = document.querySelector('.obituary_toggle')
    const events = document.querySelector('.events_toggle')
    const finances = document.querySelector('.finances_toggle')
    const complete = document.querySelector('.complete_toggle')
    deceasedInfo.style.display = "none"
    obituary.style.display = "none"
    events.style.display = "none"
    finances.style.display = "block" 
    complete.style.display = "none"
}

function completeClick(){
    const deceasedInfo = document.querySelector('.personal_info_toggle')
    const obituary = document.querySelector('.obituary_toggle')
    const events = document.querySelector('.events_toggle')
    const finances = document.querySelector('.finances_toggle')
    const complete = document.querySelector('.complete_toggle')
    deceasedInfo.style.display = "none"
    obituary.style.display = "none"
    events.style.display = "none"
    finances.style.display = "none"
    complete.style.display = "block"
}


function savePersonalInfo(deceasedId){
    const personalInfoSave = document.getElementById('personal_info_save')
    const personalInfoName = document.getElementById('personalInfoName').value
    const personalInfoAddress = document.getElementById('personalInfoAddress').value
    const personalInfoAge = document.getElementById('personalInfoAge').value
    const personalInfoDOB = document.getElementById('personalInfoDOB').value
    const personalInfoDOD = document.getElementById('personalInfoDOD').value
    const personalInfoGender = document.getElementById('personalInfoGender').value
    const personalInfoSSN = document.getElementById('personalInfoSSN').value
    const personalInfoNok = document.getElementById('personalInfoNok').value

    
    fetch(`/save_deceased_info/${deceasedId}/`,{
        method: "PUT",
        body:JSON.stringify({
            personalInfoName : personalInfoName,
            personalInfoAddress: personalInfoAddress,
            personalInfoAge: personalInfoAge, 
            personalInfoDOB: personalInfoDOB,
            personalInfoDOD: personalInfoDOD,
            personalInfoGender: personalInfoGender,
            personalInfoSSN: personalInfoSSN,
            personalInfoNok: personalInfoNok
        })
    })

    .then(response => response.json())
    .then(result => {
        
    })
}

function saveObituary(deceasedId){
    const obituary = document.getElementById('obituary').value

    fetch(`/save_obituary/${deceasedId}`,{
        method: "PUT",
        body:JSON.stringify({
            obituary: obituary
        }) 
    })
  
    .then(response => response.json())
    .then(result => {
        
    })    
}

function editProduct(product){
    console.log(document.querySelector(`#product_price_${product.id}`))
    // Once the edit button is clicked I am brought here
    // testing, everything prints
    const productPriceCurrent =  document.querySelector(`#product_price_${product.id}`).textContent.slice(1)
    const productNotesCurrent = document.querySelector(`#product_notes_${product.id}`).textContent
    const productQuantityCurrent = document.querySelector(`#product_quantity_${product.id}`).textContent
    

    const disableEdit = document.querySelector(`#product_edit_${product.id}`)
    disableEdit.style.pointerEvents = "none"
    disableEdit.style.cursor = "not-allowed"
    // when we save we should allow the button to be clicked again


    // variable name wall will be the empty div created in html where the edit product will go
    const wall = document.getElementById(`edit_product_${product.id}`)
    const wallNotes = document.getElementById(`edit_notes_${product.id}`)
    const wallQuantity = document.getElementById(`edit_quantity_${product.id}`)
    const wallPrice = document.getElementById(`edit_price_${product.id}`)
    const wallButtonEdit = document.getElementById(`edit_button_${product.id}`)
    const wallButtonCancel = document.getElementById(`cancel_button_${product.id}`)
    console.log(wallNotes)


    // create an input field for the product price

    const priceDiv = document.createElement("div")
    priceDiv.className = "input-group mb-3 edit_price_div"

    const priceSpan = document.createElement("span")
    priceSpan.className = "input-group-text edit_price_span"
    priceSpan.textContent = "Price"

    const productPrice = document.createElement("input")
    productPrice.className = "form-control edit_price"
    productPrice.value = parseFloat(productPriceCurrent)
    
    priceDiv.append(priceSpan)
    priceDiv.append(productPrice)


    const total = parseFloat(productPriceCurrent)
    const quantity = parseInt(productQuantityCurrent)

    productPrice.value = total / quantity
    
    const old_price = productPrice.value
    console.log(total)

    //TESTING ... when appending.. productNotes because productDiv in 3 places

    const notesDiv = document.createElement('div')
    notesDiv.className = "input-group mb-3 edit_notes_div"

    const productSpan = document.createElement("span")
    productSpan.className = "input-group-text edit_notes_span"
    productSpan.textContent = "Notes"

    const productNotes = document.createElement("input")
    productNotes.className = "form-control edit_notes_input"
    productNotes.value = productNotesCurrent

    notesDiv.append(productSpan)
    notesDiv.append(productNotes)

    console.log(notesDiv)
    
    // END TESTING

    const quantityDiv = document.createElement('div')
    quantityDiv.className = "input-group mb-3 edit_quantity_div"

    const quantitySpan = document.createElement('span')
    quantitySpan.className = "input-group-text edit_quantity_span"
    quantitySpan.textContent = "Quantity"

    const productQuantity = document.createElement("input")
    productQuantity.className = "form-control edit_quantity"
    productQuantity.value = productQuantityCurrent

    quantityDiv.append(quantitySpan)
    quantityDiv.append(productQuantity)


    const editProduct = document.createElement("button")
    editProduct.className = "btn btn-success"
    editProduct.textContent = "Save"

    const cancelProduct = document.createElement("button")
    cancelProduct.className = "btn btn-danger"
    cancelProduct.textContent = "Cancel"
    

    editProduct.addEventListener('click', function() {
        //save button

        const newPrice = parseFloat(productPrice.value)
        const newNotes = productNotes.value
        const newQuantity = parseInt(productQuantity.value)

  
        fetch(`/edit_product/${product.id}`, {
            method: "PUT",
            body:JSON.stringify({
                update_price: newPrice,
                update_notes: newNotes,
                update_quantity: newQuantity
            })
        })

        .then(response => response.json())
        .then(result => {
        

            priceDiv.remove()
            notesDiv.remove()
            quantityDiv.remove()
            cancelProduct.remove()
            editProduct.remove()

            disableEdit.style.pointerEvents = "auto"
            disableEdit.style.cursor = "pointer"


            
            document.querySelector(`#product_notes_${product.id}`).textContent = result.notes

            if (result.notes == null) {
                document.querySelector(`#product_notes_${product.id}`).style.display = "none"
            }
            else {
                document.querySelector(`#product_notes_${product.id}`).style.display = "block"
            }

           
            // assignment to consistant variable??? am i comparting apples to oranges here? Or is it the dollar sign?
            // text content = to $ then append the price?
            document.querySelector(`#product_price_${product.id}`).textContent = `${parseFloat(result.price).toFixed(2)}`
            console.log("@@@", document.querySelector(`#product_price_${product.id}`).textContent = `$${parseFloat(result.price).toFixed(2)}`)
            document.querySelector(`#product_quantity_${product.id}`).textContent = newQuantity


            const old_total_cost = document.querySelector("#total_cost").textContent.slice(7)


            console.log("Old Product Price (per unit): ", old_price);
            console.log("New Product Price (per Unit): ", newPrice)
            console.log("Old Product Price", total)
            console.log("New Product Price: ", result.price)
            console.log("Old Quantity: ", quantity)
            console.log("New Quantity: ", result.quantity)
            console.log("Old Total Cost: ",old_total_cost)
           

            let new_total_cost = 0

            if (old_price < result.price){

                let add_diff = result.price - total
                add_diff = add_diff.toFixed(2)
                console.log("Add-Difference", add_diff)             
                new_total_cost = parseFloat(old_total_cost) + parseFloat(add_diff)                

            }

            else {
                let sub_diff = total - result.price
                sub_diff = sub_diff.toFixed(2)
                console.log("Sub Diff: ", sub_diff)
                new_total_cost = parseFloat(old_total_cost) - parseFloat(sub_diff)
            }

            document.querySelector("#total_cost").textContent = `Total: ${new_total_cost.toFixed(2)}`
            // console.log the total
        
        })
    })

    

    cancelProduct.addEventListener('click', function() {
        disableEdit.style.pointerEvents = "auto"
        disableEdit.style.cursor = "pointer"

        priceDiv.remove()
        notesDiv.remove()
        quantityDiv.remove()
        cancelProduct.remove()
        editProduct.remove()
    })
    


    wallNotes.append(notesDiv)
    wallPrice.append(priceDiv)
    wallQuantity.append(quantityDiv)
    wallButtonEdit.append(cancelProduct)
    wallButtonEdit.append(editProduct)

    
    
}


