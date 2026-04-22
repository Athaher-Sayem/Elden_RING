let editId = null;

async function loadChars(){
    let q = document.getElementById('search').value;
    let res = await fetch('/get?q=' + q);
    let data = await res.json();

    let html = "";

    data.forEach(c => {
        html += `
        <div class="card">
            <h2>${c.name}</h2>
            <p>${c.title}</p>
            <p>⚡ Magic: ${c.magic_power}</p>
            <p>🗡 Weapon: ${c.weapon}</p>

            <button onclick="openEdit(${c.id}, '${c.name}', '${c.title}', ${c.magic_power}, '${c.weapon}')">Edit</button>
            <button onclick="deleteChar(${c.id})">Delete</button>
        </div>
        `;
    });

    document.getElementById('list').innerHTML = html;
}

async function addChar(){
    let data = {
        name: name.value,
        title: title.value,
        magic_power: magic_power.value,
        weapon: weapon.value
    };

    await fetch('/add', {
        method:'POST',
        headers:{'Content-Type':'application/json'},
        body: JSON.stringify(data)
    });

    loadChars();
}

function openEdit(id,n,t,m,w){
    editId = id;
    e_name.value = n;
    e_title.value = t;
    e_magic.value = m;
    e_weapon.value = w;
    modal.style.display = "flex";
}

function closeModal(){
    modal.style.display = "none";
}

async function saveEdit(){
    let data = {
        name: e_name.value,
        title: e_title.value,
        magic_power: e_magic.value,
        weapon: e_weapon.value
    };

    await fetch('/update/' + editId, {
        method:'POST',
        headers:{'Content-Type':'application/json'},
        body: JSON.stringify(data)
    });

    closeModal();
    loadChars();
}

async function deleteChar(id){
    await fetch('/delete/' + id, {method:'DELETE'});
    loadChars();
}

loadChars();