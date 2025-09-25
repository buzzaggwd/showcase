
document.addEventListener("DOMContentLoaded", function () {
    const options = document.querySelectorAll(".platform-option");
    const okBtn = document.getElementById("platformsOkBtn");
    const dropdownToggle = document.getElementById("filterPlatformsDropdown");
    const form = document.querySelector("form");
    const periodInput = document.getElementById("filterPeriod");

    okBtn.addEventListener("click", function () {
        let selected = "";
        options.forEach(opt => {
            if (opt.checked) {
                selected = opt.value;
            }
        });

        dropdownToggle.innerText = selected || "Выберите площадку";

        if (!selected) {
            dropdownToggle.classList.add("placeholder-style");
        } else {
            dropdownToggle.classList.remove("placeholder-style");
        }

        dropdownToggle.dataset.selectedPlatform = selected;

        const dropdown = bootstrap.Dropdown.getInstance(dropdownToggle);
        dropdown.hide();
    });

    $('#filterPeriod').daterangepicker({
        locale: {
            format: 'DD.MM.YYYY',
            applyLabel: 'Применить',
            cancelLabel: 'Отмена',
            fromLabel: 'От',
            toLabel: 'До',
            customRangeLabel: 'Выбрать период',
            daysOfWeek: ['Вс','Пн','Вт','Ср','Чт','Пт','Сб'],
            monthNames: [
                'Январь','Февраль','Март','Апрель','Май','Июнь',
                'Июль','Август','Сентябрь','Октябрь','Ноябрь','Декабрь'
            ],
            firstDay: 1
        },
        opens: 'right',
        autoUpdateInput: false
    });

    $('#filterPeriod').on('apply.daterangepicker', function(ev, picker) {
        $(this).val(
            picker.startDate.format('DD.MM.YYYY') + ' - ' + picker.endDate.format('DD.MM.YYYY')
        );
    });

    $('#filterPeriod').on('cancel.daterangepicker', function(ev, picker) {
        $(this).val('');
    });

    form.addEventListener("submit", function (e) {
        e.preventDefault();

        let selectedPlatform = dropdownToggle.dataset.selectedPlatform || "";

        let period = periodInput.value.split(" - ");
        let startDate = period[0] ? moment(period[0], "DD.MM.YYYY") : null;
        let endDate = period[1] ? moment(period[1], "DD.MM.YYYY") : null;

        document.querySelectorAll("table tbody tr").forEach(row => {
            let name = row.cells[0].innerText.trim();
            let dateCell = row.cells[1] ? row.cells[1].innerText.trim() : null;
            let date = dateCell ? moment(dateCell, "DD.MM.YYYY") : null;

            let platformMatch = !selectedPlatform || name === selectedPlatform;
            let dateMatch = true;

            if (date && startDate && endDate) {
                dateMatch = date.isBetween(startDate, endDate, "day", "[]");
            }

            row.style.display = (platformMatch && dateMatch) ? "" : "none";
        });
    });
});