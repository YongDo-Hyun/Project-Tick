Aynı şeyi cgit için mi? Tabii, çünkü herkes sabah kalkınca “bugün bir git web arayüzüne katkıda bulunayım” diye düşünüyor zaten.

cgit biraz daha “C + CGI + eski dünya düzeni” olduğu için tonunu ona göre ayarladım. Yani fazla süslü değil, ama gerçek hayatta işe yarar.

Direkt koyabileceğin **CONTRIBUTING.md**:

---

## How to Contribute to cgit

Thanks for your interest in contributing to **cgit**.

### 1. Build the project

Before making any changes, ensure that you can successfully build cgit.

Please follow the instructions in [COMPILING.md](COMPILING.md).

---

### 2. Configure and run locally

cgit is a CGI application, so you should test it in a local web server environment.

Example setup:

* Configure your web server (e.g. nginx, Apache, or lighttpd)
* Point CGI execution to the built `cgit.cgi`
* Provide a valid `cgitrc` configuration file

Verify that the interface loads correctly in your browser.

---

### 3. Make your changes

* Keep changes minimal and focused
* Follow existing C coding style
* Avoid unnecessary abstractions
* Preserve performance and low overhead
* Do not introduce heavy dependencies

---

### 4. Validate your changes

Before submitting:

* Rebuild the project
* Test via the web interface
* Check for regressions in repository browsing, diff rendering, and performance

---

### 5. Submit your contribution

* Write a clear commit message
* Please dont forget sign off your commits and <cgit:> prefix.
* Explain *why* the change is needed, not just *what* changed
* Reference related issues if applicable

---

### Notes

* cgit is designed to be simple, fast, and lightweight
* Contributions that increase complexity without clear benefit may be rejected
* Stability and performance are prioritized over new features
