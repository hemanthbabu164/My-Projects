document.addEventListener("DOMContentLoaded",function() {
    var list = document.querySelectorAll("ul li");
    list.forEach(node=> {
        node.addEventListener('click',function(event){
            const value = node.innerHTML.trim();
            const dis= document.querySelector(".Display");
            var result = dis.innerHTML.trim();
            
            if(result == '0' || result == 'undefined' || result== 'Infinity'){
                dis.innerHTML = "";  
            }
            if(value == '='){
                dis.innerHTML =  eval(result);
                return true;
            }
    
            if(value.toLowerCase() == 'c')
            {
                dis.innerHTML='';
                return true;
            }
            dis.append(value);
    
        });
    });

});