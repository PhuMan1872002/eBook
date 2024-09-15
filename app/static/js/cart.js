const addToCart = async (id, name, price) => {
    event.preventDefault()

    const res = await fetch("/api/cart/", {
        method: "post",
        body: JSON.stringify({
            "id": id,
            "title": name,
            "price": price
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    })

    const data = await res.json();
    const quantity = document.getElementsByClassName('quantity')
    const amount = document.getElementsByClassName('amount')

    for (let d of quantity)
        d.innerText = data.total_quantity;

    for (let i of amount)
        i.innerText = data.total_amount;
}

function deleteCart(id) {
    fetch(`/api/cart/${id}`, {
        method: "delete"
    }).then(function (res) {
        return res.json();
    }).then(function (data) {
        const quantity = document.getElementsByClassName('quantity')
        const amount = document.getElementsByClassName('amount')

        for (let d of quantity)
            d.innerText = data.total_quantity;

        for (let i of amount)
            i.innerText = data.total_amount;

        let t = document.getElementById(`book${id}`);
        t.style.display = "none";
    });
}

const pay = async () => {
    if (confirm("Bạn chắc chắn thanh toán?") == true) {
        const res = await fetch("/api/pay")
        const data = await res.json()
            
        if (data.status === 200)
            location.reload();
        else
            alert("Có lỗi xày ra!")
    }
}

const checkOut = async () => {
    const res = await fetch("/api/export")
    const data = await res.json()

    if (data.status === 200)
        location.reload();
    else
        alert("Có lỗi xày ra!")
}