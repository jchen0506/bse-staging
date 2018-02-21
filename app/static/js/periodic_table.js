$( document ).ready(function () {
    var table = [
        ["H", "Hydrogen", "1.00794", 1],
        ['empty', 16],
        ["He", "Helium", "4.002602", 2],
        ["Li", "Lithium", "6.941", 3],
        ["Be", "Beryllium", "9.012182", 4],
        ['empty', 10],
        ["B", "Boron", "10.811", 5],
        ["C", "Carbon", "12.0107", 6],
        ["N", "Nitrogen", "14.0067", 7],
        ["O", "Oxygen", "15.9994", 8],
        ["F", "Fluorine", "18.9984032", 9],
        ["Ne", "Neon", "20.1797", 10],
        ["Na", "Sodium", "22.98976...", 11],
        ["Mg", "Magnesium", "24.305", 12],
        ["empty", 10],
        ["Al", "Aluminium", "26.9815386", 13],
        ["Si", "Silicon", "28.0855", 14],
        ["P", "Phosphorus", "30.973762", 15],
        ["S", "Sulfur", "32.065", 16],
        ["Cl", "Chlorine", "35.453", 17],
        ["Ar", "Argon", "39.948", 18],
        ["K", "Potassium", "39.948", 19],
        ["Ca", "Calcium", "40.078", 20],
        ["Sc", "Scandium", "44.955912", 21],
        ["Ti", "Titanium", "47.867", 22],
        ["V", "Vanadium", "50.9415", 23],
        ["Cr", "Chromium", "51.9961", 24],
        ["Mn", "Manganese", "54.938045", 25],
        ["Fe", "Iron", "55.845", 26],
        ["Co", "Cobalt", "58.933195", 27],
        ["Ni", "Nickel", "58.6934", 28],
        ["Cu", "Copper", "63.546", 29],
        ["Zn", "Zinc", "65.38", 30],
        ["Ga", "Gallium", "69.723", 31],
        ["Ge", "Germanium", "72.63", 32],
        ["As", "Arsenic", "74.9216", 33],
        ["Se", "Selenium", "78.96", 34],
        ["Br", "Bromine", "79.904", 35],
        ["Kr", "Krypton", "83.798", 36],
        ["Rb", "Rubidium", "85.4678", 37],
        ["Sr", "Strontium", "87.62", 38],
        ["Y", "Yttrium", "88.90585", 39],
        ["Zr", "Zirconium", "91.224", 40],
        ["Nb", "Niobium", "92.90628", 41],
        ["Mo", "Molybdenum", "95.96", 42],
        ["Tc", "Technetium", "(98)", 43],
        ["Ru", "Ruthenium", "101.07", 44],
        ["Rh", "Rhodium", "102.9055", 45],
        ["Pd", "Palladium", "106.42", 46],
        ["Ag", "Silver", "107.8682", 47],
        ["Cd", "Cadmium", "112.411", 48],
        ["In", "Indium", "114.818", 49],
        ["Sn", "Tin", "118.71", 50],
        ["Sb", "Antimony", "121.76", 51],
        ["Te", "Tellurium", "127.6", 52],
        ["I", "Iodine", "126.90447", 53],
        ["Xe", "Xenon", "131.293", 54],
        ["Cs", "Caesium", "132.9054", 55],
        ["Ba", "Barium", "132.9054", 56],
        ["empty", 1],
        ["Hf", "Hafnium", "178.49", 72],
        ["Ta", "Tantalum", "180.94788", 73],
        ["W", "Tungsten", "183.84", 74],
        ["Re", "Rhenium", "186.207", 75],
        ["Os", "Osmium", "190.23", 76],
        ["Ir", "Iridium", "192.217", 77],
        ["Pt", "Platinum", "195.084", 78],
        ["Au", "Gold", "196.966569", 79],
        ["Hg", "Mercury", "200.59", 80],
        ["Tl", "Thallium", "204.3833", 81],
        ["Pb", "Lead", "207.2", 82],
        ["Bi", "Bismuth", "208.9804", 83],
        ["Po", "Polonium", "(209)", 84],
        ["At", "Astatine", "(210)", 85],
        ["Rn", "Radon", "(222)", 86],
        ["Fr", "Francium", "(223)", 87],
        ["Ra", "Radium", "(226)", 88],
        ["empty", 1],
        ["Rf", "Rutherfordium", "(267)", 104],
        ["Db", "Dubnium", "(268)", 105],
        ["Sg", "Seaborgium", "(271)", 106],
        ["Bh", "Bohrium", "(272)", 107],
        ["Hs", "Hassium", "(270)", 108],
        ["Mt", "Meitnerium", "(276)", 109],
        ["Ds", "Darmstadium", "(281)", 110],
        ["Rg", "Roentgenium", "(280)", 111],
        ["Cn", "Copernicium", "(285)", 112],
        ["Nh", "Unutrium", "(284)", 113],
        ["Fl", "Flerovium", "(289)", 114],
        ["Mc", "Ununpentium", "(288)", 115],
        ["Lv", "Livermorium", "(293)", 116],
        ["Ts", "Ununseptium", "(294)", 117],
        ["Og", "Ununoctium", "(294)", 118, 7],
        ["empty", 18],
        ["empty", 3],
        ["La", "Lanthanum", "138.90547", 57],
        ["Ce", "Cerium", "140.116", 58],
        ["Pr", "Praseodymium", "140.90765", 59],
        ["Nd", "Neodymium", "144.242", 60],
        ["Pm", "Promethium", "(145)", 61],
        ["Sm", "Samarium", "150.36", 62],
        ["Eu", "Europium", "151.964", 63],
        ["Gd", "Gadolinium", "157.25", 64],
        ["Tb", "Terbium", "158.92535", 65],
        ["Dy", "Dysprosium", "162.5", 66],
        ["Ho", "Holmium", "164.93032", 67],
        ["Er", "Erbium", "167.259", 68],
        ["Tm", "Thulium", "168.93421", 69],
        ["Yb", "Ytterbium", "173.054", 70],
        ["Lu", "Lutetium", "174.9668", 71],
        ["empty", 3],
        ["Ac", "Actinium", "(227)", 89],
        ["Th", "Thorium", "232.03806", 90],
        ["Pa", "Protactinium", "231.0588", 91],
        ["U", "Uranium", "238.02891", 92],
        ["Np", "Neptunium", "(237)", 93],
        ["Pu", "Plutonium", "(244)", 94],
        ["Am", "Americium", "(243)", 95],
        ["Cm", "Curium", "(247)", 96],
        ["Bk", "Berkelium", "(247)", 97],
        ["Cf", "Californium", "(251)", 98],
        ["Es", "Einstenium", "(252)", 99],
        ["Fm", "Fermium", "(257)", 100],
        ["Md", "Mendelevium", "(258)", 101],
        ["No", "Nobelium", "(259)", 102],
        ["Lr", "Lawrencium", "(262)", 103]
    ];

    table = expand_table(table);
    console.log(table);

    var periodic_table = document.getElementById("periodic_table");
    console.log(periodic_table);

    var ele_index = -1;
    for (var i=1; i<=10; i++){

        var row = get_row(periodic_table);

        var subrow = get_subrow(row);
        add_6_elements(subrow, table, ele_index);

        subrow = get_subrow(row);
        add_6_elements(subrow, table, ele_index);

        subrow = get_subrow(row);
        add_6_elements(subrow, table, ele_index);

    }

    function add_6_elements(subrow){
        for (var j=1; j<=6; j++) {
            ele_index++;

            if (table[ele_index][0] == 'empty') {
                subrow.appendChild(get_empty_slots());
            } else {
                var element = get_element(table[ele_index]);
                subrow.appendChild(element);
            }
        }
    }

    function get_empty_slots() {
        var empty_slot = document.createElement('div');
        empty_slot.className = 'col-2 cell empty_slot';
        return empty_slot;
    }

    function get_element(ele_data) {
        var cell = document.createElement('div');
        cell.className = 'col-2 cell';

        var element = document.createElement('button');
        element.id = 'element_' + ele_data[3];  // atomic number
        element.className = 'element';
        // element.style.backgroundColor = 'rgba(0,127,127,0.5)';
        element.onclick = element_clicked;
        cell.appendChild(element);

        var number = document.createElement('div');
        number.className = 'number text-right';
        number.textContent = ele_data[3] ;
        element.appendChild(number);

        var symbol = document.createElement('div');
        symbol.className = 'symbol align-middle';
        symbol.textContent = ele_data[0];
        element.appendChild(symbol);

        var details = document.createElement('div');
        details.className = 'details';
        details.innerHTML = ele_data[1] + '<br>' + ele_data[2];
        element.appendChild(details);

        return cell;
    }

    function expand_table(table) {
        var expanded = [];
        table.forEach(function (t) {
            if (t[0] != "empty"){
                expanded.push(t);
            } else {
                for (var i=0; i<t[1]; i++) expanded.push(['empty']);
            }
        });

        return expanded;
    }

    function get_row(periodic_table) {
        var row = document.createElement('div');
        row.className = 'row';
        periodic_table.appendChild(row);

        return row;
    }

    function get_subrow(parent_row) {
        var templ_col = document.createElement('div');
        templ_col.className = 'col-4';
        parent_row.appendChild(templ_col);

        var row = document.createElement('div');
        row.className = 'row';
        templ_col.appendChild(row);

        return row;
    }

    function element_clicked(e) {
        $(this).toggleClass('selected');
        e.preventDefault();
    }

    $('#reset_selection').click(function reset_selection() {
        $(".element").removeClass('selected');
        console.log('reset_selection');
    });


    $('#test_avail').click(function reset_selection() {
        $(".element").toggleClass('available');
        console.log('available');
    });
});








