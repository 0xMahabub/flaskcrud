function confirmDel(event){
    // send confirmation
    const context = event.currentTarget.getAttribute('todo')

    if(confirm('Are you sure ?')){
        console.log(context)
        window.location = '/todo/del/' + context
    } else {
        return false
    }
}

