let equipos = document.querySelector("#yw1");
equipos = equipos.querySelector("tbody");

// clubs rows in table 
equipos = equipos.querySelectorAll(".odd,.even");

// club case selector 
equipos[0].querySelector(".hauptlink .vereinprofil_tooltip");

// link to club site
equipos[0].querySelector(".hauptlink .vereinprofil_tooltip").href;

// club name 
equipos[0].querySelector(".hauptlink .vereinprofil_tooltip").text;

let clubs = {meta:["id","name","link","squad","median age","foreigners","total market value", "median market value"],data:[]};
equipos.forEach((e) => {
    let link = e.querySelector(".hauptlink .vereinprofil_tooltip").href;
    let name = e.querySelector(".hauptlink .vereinprofil_tooltip").text;
    let id = e.querySelector(".hauptlink .vereinprofil_tooltip").id;
    let metaSet = [id,name,link];
    let elementosTabla = e.querySelectorAll(".zentriert,.rechts");
    elementosTabla.forEach((elemento, index) => {
        if(index > 0 && index < 6){
            metaSet.push(elemento.innerText);
        }
    });
    clubs.data.push(metaSet);
});

tableElmnts = equipos[0].querySelectorAll(".zentriert,.rechts")
tableElmnts.forEach((e, index) => {console.log(e.innerText,index)})


JSON.stringify(clubs);

// "{"meta":["id","name","link"],"data":[["11854","Junior FC","https://www.transfermarkt.com/cd-atletico-junior/startseite/verein/11854/saison_id/2019"],["10503","Deportes Tolima","https://www.transfermarkt.com/deportes-tolima/startseite/verein/10503/saison_id/2019"],["8172","Atlético Nacional","https://www.transfermarkt.com/atletico-nacional/startseite/verein/8172/saison_id/2019"],["2352","CD América de Cali","https://www.transfermarkt.com/cd-america-de-cali/startseite/verein/2352/saison_id/2019"],["2350","Millonarios FC","https://www.transfermarkt.com/millonarios-fc/startseite/verein/2350/saison_id/2019"],["9961","Deportivo Cali","https://www.transfermarkt.com/deportivo-cali/startseite/verein/9961/saison_id/2019"],["11648","Independiente Santa Fe","https://www.transfermarkt.com/independiente-santa-fe/startseite/verein/11648/saison_id/2019"],["17425","CD La Equidad Seguros SA","https://www.transfermarkt.com/cd-la-equidad/startseite/verein/17425/saison_id/2019"],["20590","Rionegro Águilas","https://www.transfermarkt.com/itagui-ditaires/startseite/verein/20590/saison_id/2019"],["6495","Atlético Bucaramanga","https://www.transfermarkt.com/atletico-bucaramanga/startseite/verein/6495/saison_id/2019"],["10090","Asociación Deportivo Pasto","https://www.transfermarkt.com/deportivo-pasto/startseite/verein/10090/saison_id/2019"],["6984","Once Caldas","https://www.transfermarkt.com/once-caldas/startseite/verein/6984/saison_id/2019"],["39252","Jaguares de Córdoba","https://www.transfermarkt.com/jaguares-de-cordoba/startseite/verein/39252/saison_id/2019"],["10093","Independiente Medellín","https://www.transfermarkt.com/independiente-medellin/startseite/verein/10093/saison_id/2019"],["18231","Boyacá Patriotas FC","https://www.transfermarkt.com/boyaca-patriotas-fc/startseite/verein/18231/saison_id/2019"],["7136","Envigado FC","https://www.transfermarkt.com/envigado-fc/startseite/verein/7136/saison_id/2019"],["22902","Alianza Petrolera","https://www.transfermarkt.com/alianza-petrolera/startseite/verein/22902/saison_id/2019"],["14649","Boyacá Chicó FC","https://www.transfermarkt.com/boyaca-chico-fc/startseite/verein/14649/saison_id/2019"],["13379","Cúcuta Deportivo","https://www.transfermarkt.com/cucuta-deportivo/startseite/verein/13379/saison_id/2019"],["9811","Deportivo Pereira","https://www.transfermarkt.com/deportivo-pereira/startseite/verein/9811/saison_id/2019"]]}"

