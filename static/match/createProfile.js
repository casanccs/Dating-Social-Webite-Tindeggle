const ppic1 = document.querySelector('#id_ppic1');
const ppic2 = document.querySelector('#id_ppic2');
const ppic3 = document.querySelector('#id_ppic3');
const ppic4 = document.querySelector('#id_ppic4');
const ppic5 = document.querySelector('#id_ppic5');
const ppic6 = document.querySelector('#id_ppic6');
const ppic1Image = document.querySelector('#upImage1');
const ppic2Image = document.querySelector('#upImage2');
const ppic3Image = document.querySelector('#upImage3');
const ppic4Image = document.querySelector('#upImage4');
const ppic5Image = document.querySelector('#upImage5');
const ppic6Image = document.querySelector('#upImage6');

ppic2.style.display = 'none';
ppic2.toggleAttribute('hidden');
ppic3.style.display = 'none';
ppic3.toggleAttribute('hidden');
ppic4.style.display = 'none';
ppic4.toggleAttribute('hidden');
ppic5.style.display = 'none';
ppic5.toggleAttribute('hidden');
ppic6.style.display = 'none';
ppic6.toggleAttribute('hidden');

ppic1.setAttribute('onchange', 'readURL1(this)');
function readURL1(input) {
    if (input.files && input.files[0]) {
      var reader = new FileReader();
  
      reader.onload = function (e) {
        ppic1Image.setAttribute('src', e.target.result);
        ppic1Image.style.width = "150px";
        ppic1Image.style.height = "150px";
        ppic1.style.display = 'none';
        ppic1.toggleAttribute('hidden');
        ppic2.style.display = 'inline-block';
        ppic2.toggleAttribute('hidden');
      };
  
      reader.readAsDataURL(input.files[0]);
    }
  }

ppic2.setAttribute('onchange', 'readURL2(this)');
function readURL2(input) {
    if (input.files && input.files[0]) {
    var reader = new FileReader();

    reader.onload = function (e) {
        ppic2Image.setAttribute('src', e.target.result);
        ppic2Image.style.width = "150px";
        ppic2Image.style.height = "150px";
        ppic2.style.display = 'none';
        ppic2.toggleAttribute('hidden');
        ppic3.style.display = 'inline-block';
        ppic3.toggleAttribute('hidden');
    };

    reader.readAsDataURL(input.files[0]);
    }
}

ppic3.setAttribute('onchange', 'readURL3(this)');
function readURL3(input) {
    if (input.files && input.files[0]) {
      var reader = new FileReader();
  
      reader.onload = function (e) {
        ppic3Image.setAttribute('src', e.target.result);
        ppic3Image.style.width = "150px";
        ppic3Image.style.height = "150px";
        ppic3.style.display = 'none';
        ppic3.toggleAttribute('hidden');
        ppic4.style.display = 'inline-block';
        ppic4.toggleAttribute('hidden');
      };
  
      reader.readAsDataURL(input.files[0]);
    }
  }

ppic4.setAttribute('onchange', 'readURL4(this)');
function readURL4(input) {
    if (input.files && input.files[0]) {
    var reader = new FileReader();

    reader.onload = function (e) {
        ppic4Image.setAttribute('src', e.target.result);
        ppic4Image.style.width = "150px";
        ppic4Image.style.height = "150px";
        ppic4.style.display = 'none';
        ppic4.toggleAttribute('hidden');
        ppic5.style.display = 'inline-block';
        ppic5.toggleAttribute('hidden');
    };

    reader.readAsDataURL(input.files[0]);
    }
}

ppic5.setAttribute('onchange', 'readURL5(this)');
function readURL5(input) {
    if (input.files && input.files[0]) {
      var reader = new FileReader();
  
      reader.onload = function (e) {
        ppic5Image.setAttribute('src', e.target.result);
        ppic5Image.style.width = "150px";
        ppic5Image.style.height = "150px";
        ppic5.style.display = 'none';
        ppic5.toggleAttribute('hidden');
        ppic6.style.display = 'inline-block';
        ppic6.toggleAttribute('hidden');
      };
  
      reader.readAsDataURL(input.files[0]);
    }
  }

ppic6.setAttribute('onchange', 'readURL6(this)');
function readURL6(input) {
    if (input.files && input.files[0]) {
    var reader = new FileReader();

    reader.onload = function (e) {
        ppic6Image.setAttribute('src', e.target.result);
        ppic6Image.style.width = "150px";
        ppic6Image.style.height = "150px";
        ppic6.style.display = 'none';
        ppic6.toggleAttribute('hidden');
    };

    reader.readAsDataURL(input.files[0]);
    }
}