import {service} from "./js/datebaseConfig.js"

const endPoint = "/Regador"

// Definindo estrutura do corpo do meu objeto do banco.
var body = {
    
}

// Carregando dados do meu banco
const loadData = () => {
    service.load(endPoint).then( data => {
        body = data;
        // console.log(body);

        const rooms = ['Planta1']
        rooms.forEach(room => {
            // getLightsValues(room)
            // getTvValues(room)
            setTempValues(room)
        });
    })
}
// Definindo os dados no meu banco.
// service.set(endPoint, body)

// ==================  Colocando os dados no HTML   ==================
// const getLightsValues = (idLocal) => {
//     let lamp = document.getElementById('lightBulb' + idLocal)
//     let lightOn = false;

//     switch (idLocal) {
//         case 'LivingRoom':
//             lightOn = body.livingRoom.principalLight;
//             break;
//         case 'Office':
//             lightOn = body.office.principalLight;
//             break;
//         case 'PrincipalRoom':
//             lightOn = body.principalRoom.principalLight;
//             break;
//     }

//     if(lightOn){ 
//         lamp.classList.add("light-on")
//     } else {
//         lamp.classList.remove("light-on")
//     }
// }

// const getTvValues = (idLocal) => {
//     let tv = document.getElementById(idLocal + "Tv")
//     let tvOn = false;

//     switch (idLocal) {
//         case 'LivingRoom':
//             tvOn = body.livingRoom.tv;
//             break;
//         case 'Office':
//             tvOn = body.office.tv;
//             break;
//         case 'PrincipalRoom':
//             tvOn = body.principalRoom.tv;
//             break;
//     }

//     if(tvOn){ 
//         tv.innerHTML = 'On'
//     } else {
//         tv.innerHTML = 'OFF'
//     }
// }

const setTempValues = (idLocal) => {
    const TempElement = document.getElementById(idLocal + "Temperatura")
    const HumidElement = document.getElementById(idLocal + "UmidadeSolo")

    let Hvalue = 0;
    let Tvalue = 0;

    switch (idLocal) {
        case 'Planta1':
            Hvalue = body.Planta1.UmidadeSolo;
            Tvalue = body.Planta1.Temperatura;
            break;
    
        case 'Planta2':
            Hvalue = body.Planta2.UmidadeSolo;
            Tvalue = body.Planta2.Temperatura;
            break;
    
        case 'Planta3':
            Hvalue = body.Planta3.UmidadeSolo;
            Tvalue = body.Planta3.Temperatura;
            break;
    
        default:
            break;
    }
    
    TempElement.innerHTML = Tvalue
    HumidElement.innerHTML = Hvalue
}

// ================== Funções de Interação com HTML ==================


const Regar = () => {
    let value = body.Repor 

    if(value == 0)
    {
        body.Repor = 1
        service.set(endPoint, body)

    } else {
        body.Repor = 0
        service.set(endPoint, body)

    }

    // switch (idRoom) {
    //     case "Planta1":
    //         body.Planta1.principalLight = !body.Planta1.principalLight;
    //         service.set(endPoint, body);
    //         break;
            
    //     case 'Planta2' :
    //         body.Planta2.principalLight = !body.Planta2.principalLight;
    //         service.set(endPoint, body);
    //         break;

    //     case 'Planta3' :
    //         body.Planta3.principalLight = !body.Planta3.principalLight;
    //         service.set(endPoint, body);
    //         break;

    //     default:
    //         break;
}

// const toggleTv = (idRoom) => {
//     const element = document.getElementById(idRoom + "Tv")
//     let isOn = false;
//     switch (idRoom) {
//         case "LivingRoom":
//             body.livingRoom.tv = !body.livingRoom.tv;
//             isOn = body.livingRoom.tv;
//             service.set(endPoint, body);
//             break;
            
//         case 'Office' :
//             body.office.tv = !body.office.tv;
//             isOn = body.office.tv;
//             service.set(endPoint, body);
//             break;

//         case 'PrincipalRoom' :
//             body.principalRoom.tv = !body.principalRoom.tv;
//             isOn = body.principalRoom.tv;
//             service.set(endPoint, body);
//             break;

//         default:
//             break;
//     }
//     if(isOn) {
//         element.innerHTML = "ON"
//     } else {
//         element.innerHTML = "OFF"
//     }
// }

console.log('script loaded');

//! Adicionando as funções no HTML 

// window.toggleLamp = toggleLamp
// window.toggleTv = toggleTv
window.setTempValues = setTempValues
window.Regar = Regar

setInterval(() => {
    loadData();
}, 2000);