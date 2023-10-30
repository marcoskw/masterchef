function confirmation(){
    const forms = document.querySelectorAll('.form-delete');
    
    for(const form of forms) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();

            const confirmed = confirm('Você tem certeza que quer apagar esta receita?')

            if (confirmed) {
                form.submit();
            }
        }); 
    }
}

confirmation();