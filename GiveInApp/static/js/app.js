document.addEventListener("DOMContentLoaded", function () {
    /**
     * HomePage - Help section
     */
    class Help {
        constructor($el) {
            this.$el = $el;
            this.$buttonsContainer = $el.querySelector(".help--buttons");
            this.$slidesContainers = $el.querySelectorAll(".help--slides");
            this.currentSlide = this.$buttonsContainer.querySelector(".active").parentElement.dataset.id;
            this.init();
        }

        init() {
            this.events();
        }

        events() {
            /**
             * Slide buttons
             */
            this.$buttonsContainer.addEventListener("click", e => {
                if (e.target.classList.contains("btn")) {
                    this.changeSlide(e);
                }
            });

            /**
             * Pagination buttons
             */
            this.$el.addEventListener("click", e => {
                if (e.target.classList.contains("btn") && e.target.parentElement.parentElement.classList.contains("help--slides-pagination")) {
                    this.changePage(e);
                }
            });
        }

        changeSlide(e) {
            e.preventDefault();
            const $btn = e.target;

            // Buttons Active class change
            [...this.$buttonsContainer.children].forEach(btn => btn.firstElementChild.classList.remove("active"));
            $btn.classList.add("active");

            // Current slide
            this.currentSlide = $btn.parentElement.dataset.id;

            // Slides active class change
            this.$slidesContainers.forEach(el => {
                el.classList.remove("active");

                if (el.dataset.id === this.currentSlide) {
                    el.classList.add("active");
                }
            });
        }

        /**
         * TODO: callback to page change event
         */
        changePage(e) {
            e.preventDefault();
            const page = e.target.dataset.page;

            console.log(page);
        }
    }

    const helpSection = document.querySelector(".help");
    if (helpSection !== null) {
        new Help(helpSection);
    }

    /**
     * Form Select
     */
    class FormSelect {
        constructor($el) {
            this.$el = $el;
            this.options = [...$el.children];
            this.init();
        }

        init() {
            this.createElements();
            this.addEvents();
            this.$el.parentElement.removeChild(this.$el);
        }

        createElements() {
            // Input for value
            this.valueInput = document.createElement("input");
            this.valueInput.type = "text";
            this.valueInput.name = this.$el.name;

            // Dropdown container
            this.dropdown = document.createElement("div");
            this.dropdown.classList.add("dropdown");

            // List container
            this.ul = document.createElement("ul");

            // All list options
            this.options.forEach((el, i) => {
                const li = document.createElement("li");
                li.dataset.value = el.value;
                li.innerText = el.innerText;

                if (i === 0) {
                    // First clickable option
                    this.current = document.createElement("div");
                    this.current.innerText = el.innerText;
                    this.dropdown.appendChild(this.current);
                    this.valueInput.value = el.value;
                    li.classList.add("selected");
                }

                this.ul.appendChild(li);
            });

            this.dropdown.appendChild(this.ul);
            this.dropdown.appendChild(this.valueInput);
            this.$el.parentElement.appendChild(this.dropdown);
        }

        addEvents() {
            this.dropdown.addEventListener("click", e => {
                const target = e.target;
                this.dropdown.classList.toggle("selecting");

                // Save new value only when clicked on li
                if (target.tagName === "LI") {
                    this.valueInput.value = target.dataset.value;
                    this.current.innerText = target.innerText;
                }
            });
        }
    }

    document.querySelectorAll(".form-group--dropdown select").forEach(el => {
        new FormSelect(el);
    });

    /**
     * Hide elements when clicked on document
     */
    document.addEventListener("click", function (e) {
        const target = e.target;
        const tagName = target.tagName;

        if (target.classList.contains("dropdown")) return false;

        if (tagName === "LI" && target.parentElement.parentElement.classList.contains("dropdown")) {
            return false;
        }

        if (tagName === "DIV" && target.parentElement.classList.contains("dropdown")) {
            return false;
        }

        document.querySelectorAll(".form-group--dropdown .dropdown").forEach(el => {
            el.classList.remove("selecting");
        });
    });

    /**
     * Switching between form steps
     */
    class FormSteps {
        constructor(form) {
            this.$form = form;
            this.$next = form.querySelectorAll(".next-step");
            this.$prev = form.querySelectorAll(".prev-step");
            this.$step = form.querySelector(".form--steps-counter span");
            this.currentStep = 1;

            this.$stepInstructions = form.querySelectorAll(".form--steps-instructions p");
            const $stepForms = form.querySelectorAll("form > div");
            this.slides = [...this.$stepInstructions, ...$stepForms];

            this.init();
        }

        /**
         * Init all methods
         */
        init() {
            this.events();
            this.updateForm();
        }

        /**
         * All events that are happening in form
         */
        events() {
            // Next step
            this.$next.forEach(btn => {
                btn.addEventListener("click", e => {
                    e.preventDefault();
                    this.currentStep++;
                    this.updateForm();
                });
            });

            // Previous step
            this.$prev.forEach(btn => {
                btn.addEventListener("click", e => {
                    e.preventDefault();
                    this.currentStep--;
                    this.updateForm();
                });
            });

            // Form submit
            this.$form.querySelector("form").addEventListener("submit", e => this.submit(e));
        }

        /**
         * Update form front-end
         * Show next or previous section etc.
         */
        updateForm() {
            this.$step.innerText = this.currentStep;

            // TODO: Validation

            this.slides.forEach(slide => {
                slide.classList.remove("active");

                if (slide.dataset.step == this.currentStep) {
                    slide.classList.add("active");
                }
            });

            this.$stepInstructions[0].parentElement.parentElement.hidden = this.currentStep >= 6;
            this.$step.parentElement.hidden = this.currentStep >= 6;

            // TODO: get data from inputs and show them in summary
        }

        /**
         * Submit form
         *
         * TODO: validation, send data to server
         */
        // submit(e) {
        //     e.preventDefault();
        //     this.currentStep++;
        //     this.updateForm();
        // }
    }

    const form = document.querySelector(".form--steps");
    if (form !== null) {
        new FormSteps(form);
    }

    // Checking if value is int or parsable to int
    function is_int(value) {
        return (parseInt(value) % 1 === 0);
    }

    const form_checkboxes = document.querySelectorAll("#form_1_step input")


    let FirstStepFormArray = []
    document.querySelector("#form_1_step button").addEventListener("click", function () {
        FirstStepFormArray = []
        form_checkboxes.forEach(function (checkbox) {
            if (checkbox.checked === true) {
                FirstStepFormArray.push(parseInt(checkbox.value))
            }
        })
    })
    document.querySelector("#form_1_step button").addEventListener("click", function () {
        const Institutions = document.querySelectorAll("#form_3_step")
        Institutions.forEach(function (institution) {
            let category = institution.querySelectorAll("#category")
            let arr = []
            for (let i in category) {
                if (is_int(category[i].innerText)) {
                    arr.push(parseInt(category[i].innerText))
                }
            }
            if (!(FirstStepFormArray.every(elem => arr.includes(elem)))) {
                institution.style.display = "none"
            }
        })
    })

    // Summary of the form
    const summary_delivery_adress = document.querySelectorAll("#delivery_address li");
    const summary_delivery_time = document.querySelectorAll("#delivery_time li");
    const summary_text = document.querySelectorAll("#form_summary .summary .summary--text");
    const summary_button = document.querySelector("#summary_button ");

    const checkboxes = document.querySelectorAll("#checkbox_form");
    const bag_amount = document.querySelector("#bag_amount");
    const institutions = document.querySelectorAll("#form_3_step input")
    const delivery_adress = document.querySelectorAll("#address_form input");
    const delivery_time = document.querySelectorAll("#delivery_time input")


    summary_button.addEventListener("click", function () {
        let checkbox_items = []
        checkboxes.forEach(function (checkbox) {
            if (checkbox.querySelector('input').checked) {
                checkbox_items.push(checkbox.children[2].innerText)
            }
        })
        summary_text[0].innerText = bag_amount.value + " " + "worków" + " zawierających " + checkbox_items

        let institution_name = []
        institutions.forEach(function (institution) {
            if (institution.checked) {
                institution_name.push(institution.parentNode.children[2].children[0].innerText)
            }
        })
        summary_text[1].innerText = "Dla " + institution_name

        let deli_adress = []
        delivery_adress.forEach(function (address) {
            deli_adress.push(address.value)
        })
        for (let i = 0; i < 4; i++) {
            summary_delivery_adress[i].innerText = deli_adress[i]
        }

        let deli_time = []
        delivery_time.forEach(function (time) {
            deli_time.push(time.value)
        })
        const textarea = document.getElementById("mytextarea").value
        for (let i = 0; i < 2; i++) {
            summary_delivery_time[i].innerText = deli_time[i]
        }
        summary_delivery_time[2].innerText = textarea
    })

});
