/**
 *
 */

// Load Basis set metadata
jQuery.ajax({
    url: "web_metadata/",
    data: '',
    contentType: "application/json",
    dataType: "json",
    success: function(result) {
        console.log("Returned data", result);
        window.bs_metadata = result['metadata'];
        window.element_basis = result['element_basis'];
    } // success
}); // ajax


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

    var periodic_table = document.getElementById("periodic_table");
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
            if (t[0] !== "empty"){
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

    $('#basis_sets').change(function () {
        basis_sets_selection_changed();
    });

    function basis_sets_selection_changed() {
        // change the table based on new basis set selection

        var selected = $('#basis_sets').find(":selected").val();
        console.log('Selected bs: ', selected);

        // update summary card
        update_summary(selected);

        if (! selected){
            $(".element").removeClass('available');
            return;
        }
        var elements = window.bs_metadata[selected][0].elements;

        $(".element").removeClass('available');
        elements.forEach(function (element) {
           $('#element_'+element).addClass('available');
        });

    }

    function update_summary(selected) {
        // TODO: update summary card with bass set data
        $('#basis_set_name').text(selected? selected : '');
    }

    function element_clicked(e) {
        $(this).toggleClass('selected');
        e.preventDefault();
        // update basis sets filter
        if (! $(this).hasClass('available')){
            filter_basis_set_names(true);
        }else{
            filter_basis_set_names(false);
        }
    }

    $('#reset_selection').click(function () {
        $(".element").removeClass('selected');
        filter_basis_set_names(false);
    });


    $('#select_all_avail').click(function () {
        // Only to available elements
        $(".element.available").addClass('selected');
        filter_basis_set_names(false);
    });

    $('#search_name').keyup(function () {
        filter_basis_set_names(true);
    });

    function filter_basis_set_names(reset_available) {
        // show only the basis set that has the search filter keyword
        // and available according to selected elements

        // filtering
        var id;
        var filter = $('#search_name').val().toUpperCase();
        var options = $('#basis_sets').find('option');
        var available_bs = '';
        var selected_elements = $('.element.selected');

        if (selected_elements.length > 0){
            // assign list to first element's basis sets
            id = $(selected_elements[0]).prop('id').split('_')[1];
            available_bs = window.element_basis[id];
            selected_elements.each(function (e) {
                id = $(this).prop('id').split('_')[1];  // get the number from "element_x"
                available_bs = _.intersection(available_bs, window.element_basis[id]);
            });
        }

        if (reset_available) {
            // Remove available
            $('.element').removeClass('available');
            // remove selected basis sets
            $('#basis_sets').val('');
            basis_sets_selection_changed();  // event listener trigger is not working
        }

        var option;
        for (var i=0; i< options.length; i++){
            option = $(options[i]).text();
            if (option.toUpperCase().indexOf(filter) === -1 ||
                (selected_elements.length > 0 && available_bs.indexOf(option) === -1)) {
                $(options[i]).addClass('d-none');
            }else{
                $(options[i]).removeClass('d-none');
            }
        }
    }

    $("#get_basis_sets").click(function (e) {

        e.preventDefault();
        var query = '';
        var url = "get_basis_set/";
        var basis_set = $('#basis_sets').val();
        var format = $('#format').val();
        var optimize = $('#optimize').val();
        var elements = $('.element.selected');

        if (! basis_set){
            alert("Please click on the basis set you want to download.");
            return;
        }

        if ( elements.length === 0){
            alert("Please click on the element buttons to select/unselect elements you want to include for download.");
            return;
        }
        var elements_ids = [];
        elements.each(function (e) {
            elements_ids.push($(this).prop('id').split('_')[1]);
        });
        console.log('after: ', elements_ids, 'toString: ', elements_ids.toString());

        query += basis_set + '/elements/' + elements_ids.toString() + '/format/' + format + '/?';

        if (optimize){
            query += '&uncontract_general=' + optimize;
        }

        console.log('Download Basis set for query: ', query);
        window.open(url + query, 'Basis Set ' + basis_set, "height=650,width=600");

        // // ajax to get basis set
        // jQuery.ajax({
        //     url: url,
        //     data: '',
        //     contentType: "application/json",
        //     success: function(result) {
        //         console.log("Returned data", result);
        //         // download data ---->
        //     } // success
        // }); // ajax

    });


});








