
      function ComboBoxCore(e, l){
        var editField = e;
        var list = l;
        var closeList;
        var completionActive = false;
        var previousLength = 0;
        var lastLength = 0;
        var textList;

        var closeComboBoxList = function() {
          list.style.visibility = "hidden";
          list.style.display = "none";
          list.disabled = true;
        }

        this.openComboBoxList = function(){
          if (closeList) window.clearTimeout(closeList);
          list.style.visibility = "visible";
          list.style.display = "block";
          list.disabled = false;
          return false;
        }

        this.initCloseComboBoxList = function() {
          closeList = window.setTimeout(closeComboBoxList,1200);
          return false;
        }

        this.onfocusComboBoxList = function() {
          if (closeList) window.clearTimeout(closeList);
          return false;
        }

        this.updateList2EditField = function() {
          if(list.selectedIndex>=0)
            editField.value = list
[list.selectedIndex].text;
          editField.focus();
          editField.select();
          return false;
        }

        var completionComboBox = function(prefix, completion){
          editField.value = prefix;
          if(typeof document.selection != 'undefined') {
            var range = document.selection.createRange();
            range.text = completion;
            range.moveStart('character', -completion.length);
            range.select();
          } else if(typeof editField.selectionStart != 'undefined'){
            var i = editField.value.length;
            editField.value += completion;
            editField.selectionStart = i;
          }
        }

        var convert = function(w) {
           var word = w.toUpperCase();
           word=word.replace(/[\u00C0\u00C1\u00C2\u00C3\u00C4\u00C5\u00C6]/gi,'A');
           word=word.replace(/[\u00C7]/gi,'C');
           word=word.replace(/[\u00C8\u00C9\u00CA\u00CB]/gi,'E');
           word=word.replace(/[\u00CC\u00CD\u00CE\u00CF]/gi,'I');
           word=word.replace(/[\u00D1]/gi,'N');
           word=word.replace(/[\u00D2\u00D3\u00D4\u00D5\u00D6]/gi,'O');
           word=word.replace(/[\u00D9\u00DA\u00DB\u00DC]/gi,'U');
           /*word=word.replace(/[\u00E0\u00E1\u00E2\u00E3\u00E4\u00E5\u00E6]/gi,'a');
           word=word.replace(/[\u00E7]/gi,'c');
           word=word.replace(/[\u00E8\u00E9\u00EA\u00EB]/gi,'e');
           word=word.replace(/[\u00EC\u00ED\u00EE\u00EF]/gi,'i');
           word=word.replace(/[\u00F1]/gi,'n');
           word=word.replace(/[\u00F2\u00F3\u00F4\u00F5\u00F6]/gi,'o');
           word=word.replace(/[\u00F9\u00FA\u00FB\u00FC]/gi,'u');*/
           return word;
        }

        this.searchEditFieldIn2List = function(){
          var i = 0;
          var value = editField.value;
          var listValue;
          var prefix;

          if (lastLength == value.length){
            completionActive = false;
            previousLength = 0;
            return false;
          }

          if ((completionActive == true)&&(value.length == previousLength))
            editField.value = value.substr(0, value.length-1);

          if (editField.value == 0){
            completionActive = false;
            previousLength = 0;
            lastLength = 0;
            list.selectedIndex = -1;
            return false;
          }

          value = convert(editField.value);
          while (value > textList[i])++i;
          list[i].selected = true;

          listValue = list[i].text;
          prefix = listValue.substr(0, value.length);
          if (convert(prefix) == value){
            completionActive = true;
            previousLength = value.length;
            completionComboBox(prefix, listValue.slice(value.length));
          }else{
            completionActive = false;
            previousLength = 0;
          }
          lastLength = editField.value.length;
          editField.focus();
          return false;
        }

        this.init = function(){
          textList = new Array(list.options.length);

          for (var i=0; i < list.options.length; ++i){
            textList[i] = convert(list[i].text);
          }
        }
      }

      function ComboBox(e, l){
        this.editField = e;
        this.list = l;
        var combo = new ComboBoxCore(this.editField, this.list);

        combo.init();

        this.list.comboBox = combo;
        this.editField.comboBox = combo;

        this.list.onchange = function(){return this.comboBox.updateList2EditField();};
        this.list.onblur = function(){return this.comboBox.initCloseComboBoxList();};
        this.list.onfocus = function(){return this.comboBox.onfocusComboBoxList();};

        this.editField.onfocus = function(){return this.comboBox.openComboBoxList();};
        this.editField.onblur = function(){return this.comboBox.initCloseComboBoxList();};
        this.editField.onkeyup = function(){return this.comboBox.searchEditFieldIn2List();};
      }
