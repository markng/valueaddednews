// Value Added Label widget
//
// A javascript widget to embed on a page, which shows hNews information
// for articles in a little pop-up box.
// 
// See: http://valueaddednews.org/technical/newslabel
// Author: Ben Campbell (Media Standards Trust)
//

//======================================================

// Generic Microformat Parser v0.1 Dan Webb (dan@danwebb.net)
// Licenced under the MIT Licence
// 
// var people = HCard.discover();
// people[0].fn => 'Dan Webb'
// people[0].urlList => ['http://danwebb.net', 'http://eventwax.com']
//
// TODO
//
// Fix _propFor to work with old safari
// Find and use unit testing framework on microformats.org test cases
// isue with hcard email?
// More formats: HFeed, HEntry, HAtom, RelTag, XFN?

// Changes by BenC (pending sending a patch back to Dan ;-):
// in parseISO8601():
//  - added base specifier to ParseInt() calls
//   (thanks, http://jehiah.cz/archive/javascript-parseint-is-broken !)
//  - "part" variable now local scope
// added a "postprocess" function to definition spec/format

// JavaScript 1.6 Iterators and generics cross-browser
if (!Array.prototype.forEach) {
  Array.prototype.forEach = function(func, scope) {
    scope = scope || this;
    for (var i = 0, l = this.length; i < l; i++)
      func.call(scope, this[i], i, this); 
  }
}

if (typeof Prototype != 'undefined' || !Array.prototype.map) {
  Array.prototype.map = function(func, scope) {
    scope = scope || this;
    var list = [];
    for (var i = 0, l = this.length; i < l; i++)
        list.push(func.call(scope, this[i], i, this)); 
    return list;
  }
}

if (typeof Prototype != 'undefined' || !Array.prototype.filter) {
  Array.prototype.filter = function(func, scope) {
    scope = scope || this;
    var list = [];
    for (var i = 0, l = this.length; i < l; i++)
        if (func.call(scope, this[i], i, this)) list.push(this[i]); 
    return list;
  }
}

['forEach', 'map', 'filter', 'slice', 'concat'].forEach(function(func) {
    if (!Array[func]) Array[func] = function(object) {
      return this.prototype[func].apply(object, Array.prototype.slice.call(arguments, 1));
    }
});

// ISO8601 Date extension
Date.ISO8601PartMap = {
  Year : 1,
  Month : 3,
  Date : 5,
  Hours : 7,
  Minutes : 8,
  Seconds : 10
}

Date.matchISO8601 = function(text) { 
  return text.match(/^(\d{4})(-?(\d{2}))?(-?(\d{2}))?(T(\d{2}):?(\d{2})(:?(\d{2}))?)?(Z?(([+\-])(\d{2}):?(\d{2})))?$/); 
}

Date.parseISO8601 = function(text) {
  var dateParts = this.matchISO8601(text);
  if (dateParts) {
    var date = new Date, part, parts, offset = 0;
    for (var prop in this.ISO8601PartMap) {
      if ( part = dateParts[this.ISO8601PartMap[prop]]) 
        date['set' + prop]((prop == 'Month') ? parseInt(part,10)-1 : parseInt(part,10));
        else date['set' + prop]((prop == 'Date') ? 1 : 0);
    }
    if (dateParts[11]) {
      offset = (parseInt(dateParts[14],10) * 60) + parseInt(dateParts[15],10);
      offset *= ((dateParts[13] == '-') ? 1 : -1);
    }
    
    offset -= date.getTimezoneOffset();
    date.setTime(date.getTime() + (offset * 60 * 1000)); 
    
    return date;
  }
}

// Main Microformat namespace
Microformat = {
  define : function(name, spec) {
    var mf = function(node, data) {
      this.parentElement = node;
      Microformat.extend(this, data);
    };
    
    mf.container = name;
    mf.format = spec;
    mf.prototype = Microformat.Base;
    return Microformat.extend(mf, Microformat.SingletonMethods);
  },
  SingletonMethods : {
    discover : function(context) {
      return Microformat.$$(this.container, context).map(function(node) {
        return new this(node, this._parse(this.format, node));
      }, this);
    },
    _parse : function(format, node) {
      var data = {};
      this._process(data, format.one, node, true);
      this._process(data, format.many, node);
      if( format.postprocess ) {
        format.postprocess( data, node ) }
      return data;
    },
    _process : function(data, format, context, firstOnly) {
      var selection, first;
      format = format || [];
      format.forEach(function(item) {
        if (typeof item == 'string') {
          selection = Microformat.$$(item, context);
          
          if (firstOnly && (first = selection[0])) {
            data[this._propFor(item)] = this._extractData(first, 'simple', data);
          } else if (selection.length > 0) {
            data[this._propFor(item) + 'List'] = selection.map(function(node) {
              return this._extractData(node, 'simple', data);
            }, this);
          }
            
        } else {
          
            for (var cls in item) {
              selection = Microformat.$$(cls, context);
              
              if (firstOnly && (first = selection[0])) {
                data[this._propFor(cls)] = this._extractData(first, item[cls], data);
              } else if (selection.length > 0) {
                data[this._propFor(cls + 'List')] = selection.map(function(node) {
                  return this._extractData(node, item[cls], data);
                }, this);
              }
            }
              
        }
        
      }, this);
      return data;
    },
    _extractData : function(node, dataType, data) {
      if (dataType._parse) return dataType._parse(dataType.format, node);
      if (typeof dataType == 'function') return dataType.call(this, node, data);
      
      var values = Microformat.$$('value', node);
      if (values.length > 0) return this._extractClassValues(node, values);
      
      switch (dataType) {
        case 'simple': return this._extractSimple(node);
        case 'url': return this._extractURL(node);
      }
      return this._parse(dataType, node);
    },
    _extractURL : function(node) {
      var href;
      switch (node.nodeName.toLowerCase()) {
        case 'img':    href = node.src;
                       break;
        case 'area':
        case 'a':      href = node.href;
                       break;
        case 'object': href = node.data;
      }
      if (href) {
        if (href.indexOf('mailto:') == 0) 
          href = href.replace(/^mailto:/, '').replace(/\?.*$/, '');
        return href;
      }
      
      return this._coerce(this._getText(node));
    },
    _extractSimple : function(node) {
      switch (node.nodeName.toLowerCase()) {
        case 'abbr': return this._coerce(node.title);
        case 'img': return this._coerce(node.alt);
      }
      return this._coerce(this._getText(node));
    },
    _extractClassValues : function(node, values) {
      var value = new String(values.map(function(value) {
        return this._extractSimple(value);
      }, this).join(''));
      var types = Microformat.$$('type', node);
      var t = types.map(function(type) {
        return this._extractSimple(type);
      }, this);
      value.types = t;
      return value;
    },
    _getText : function(node) {
      if (node.innerText) return node.innerText;
      return Array.map(node.childNodes, function(node) {
        if (node.nodeType == 3) return node.nodeValue;
        else return this._getText(node);
      }, this).join('').replace(/\s+/g, ' ').replace(/(^\s+)|(\s+)$/g, '');
    },
    _coerce : function(value) {
      var date, number;
      if (value == 'true') return true;
      if (value == 'false') return false;
      if (date = Date.parseISO8601(value)) return date;
      return String(value);
    },
    _propFor : function(name) {
      this.__propCache = this.__propCache || {};
      if (prop = this.__propCache[name]) return prop;
      return this.__propCache[name] = name.replace(/(-(.))/g, function() {
        // this isn't going to work on old safari without the fix....hmmm
        return arguments[2].toUpperCase();
      });
    },
    _handle : function(prop, item, data) {
      if (this.handlers[prop]) this.handlers[prop].call(this, item, data);
    }
  },
  // In built getElementsByClassName
  $$ : function(className, context) {
    context = context || document;
    var nodeList;

    if (context == document || context.nodeType == 1) {
      if (typeof document.evaluate == 'function') {
        var xpath = document.evaluate(".//*[contains(concat(' ', @class, ' '), ' " + className + " ')]", 
                                      context, null, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE, null);
        var els = [];
        for (var i = 0, l = xpath.snapshotLength; i < l; i++)
         els.push(xpath.snapshotItem(i));
        return els;
      } else nodeList = context.getElementsByTagName('*');
    } else nodeList = context;

    var re = new RegExp('(^|\\s)' + className + '(\\s|$)');
    return Array.filter(nodeList, function(node) {  return node.className.match(re) });
  },
  // In built Object.extend equivilent
  extend : function(dest, source) {
    for (var prop in source) dest[prop] = source[prop];
    return dest;
  },
  // methods available to all instances of a microformat
  Base : {}
};

//==================================
// Dan webbs's HCard spec

var HCard = Microformat.define('vcard', {
  one : ['bday', 'tz', 'sort-string', 'uid', 'class', {
    'n' : {
      one : ['family-name', 'given-name', 'additional-name'],
      many : ['honorific-prefix', 'honorific-suffix']
    },
    'geo' : function(node) {
      var m;
      if ((node.nodeName.toLowerCase() == 'abbr') && (m = node.title.match(/^([\-\d\.]+);([\-\d\.]+)$/))) {
        return { latitude : m[1], longitude : m[2] };
      }
      
      return this._extractData(node, { one : ['latitude', 'longitude'] });
    },
    // implied n
    'fn' : function(node, data) {
      var m, fn = this._extractData(node, 'simple');
      
      if (m = fn.match(/^(\w+) (\w+)$/)) {
        data.n = data.n || {};
        data.n.givenName = data.n.givenName || m[1];
        data.n.familyName = data.n.familyName || m[2];
      }
      
      if (m = fn.match(/^(\w+),? (\w+)\.?$/)) {
        data.n = data.n || {};
        data.n.givenName = data.n.givenName || m[2];
        data.n.familyName = data.n.familyName || m[1];
      }
      
      return fn;
    }
  }],
  many : ['label', 'sound', 'title', 'role', 'key', 'mailer', 'rev', 'nickname', 'category', 'note', 'tel', { 
      'url' : 'url', 'logo' : 'url', 'photo' : 'url', 'email' : 'url' 
    }, {
    'adr' : {
      one : ['post-office-box', 'extended-address', 'street-address', 'locality', 'region',
             'postal-code', 'country-name']
    },
    // implied org
    'org' : function(node) {
      var org = this._extractData(node, {
        one : ['organization-name'],
        many : ['organization-unit']
      });
      
      if (!org.organizationName) 
        org.organizationName = this._extractData(node, 'simple');
        
      return org;
    }
  }]
});



//==============================================
//


var HNews = Microformat.define('hentry', {
  one : ['entry-title', 'entry-summary', 'published', 'updated' ],
  many : [ {'author' : HCard} ],
  postprocess : function( data,node ) {
    // implied updated
    if( data.published && !data.updated ) {
        data.updated=data.published;
    }

    // look for statement-of-principles
    // TODO: uF parser has no built-in support for rel-blah patterns... should add
    // it properly rather than special casing it like this!
    var links = node.getElementsByTagName("a");
    for (var i = 0; i<links.length; ++i) {
        if( links[i].getAttribute('rel') == 'principles' ) {
            data.principles = { url: links[i].href, name: links[i].innerHTML };
        }
    }
  }
});




VAB = {
// Use Dan Webb's getElementsByClassName instead of defining our own!
getElementsByClassName: Microformat.$$,

getElementByClassName: function( className, context ) {
    l = VAB.getElementsByClassName( className, context );
    if( l.length == 0 ) {
        return undefined;
    } else {
        return l[0];
    }
},

createShowFunction: function( popup ) {
    return function() { popup.style.display = 'block'; }
},
createHideFunction: function( popup ) {
    return function() { popup.style.display = 'none'; }
},

go: function() {
    var root = "http://valueaddednews.org";

    // pull in our stylesheet
    var headID = document.getElementsByTagName("head")[0];
    var cssNode = document.createElement('link');
    cssNode.type = 'text/css';
    cssNode.rel = 'stylesheet';
    cssNode.href = root + '/css/vab.css';
    headID.appendChild(cssNode);


    // add events to container(s)
    var containers = VAB.getElementsByClassName( 'vab-container' );
    var popups = []
    for( var i=0; i<containers.length; ++i )
    {
        var c = containers[i];
        var p = VAB.getElementByClassName('vab-popup', c );
        popups.push( p );
        c.onmouseover = VAB.createShowFunction(p);
        c.onmouseout = VAB.createHideFunction(p);
    }


    // look for articles on page:
    var stories = HNews.discover();

    // if more stories that containers, drop some
    if( stories.length > containers.length ) {
        stories = stories.slice( 0, containers.length);
    }


    // now write out story data to the popups!
    for( var i=0; i<stories.length; ++i ) {
        var story_html = VAB.renderIngredients( stories[i] );
        popups[i].innerHTML = story_html;
    }
},

fmtRow: function( name, value ) {
    var out = '<tr class="' + (rowcnt&1 ? 'vab-odd':'vab-even') + '">';
    out = out + '<td class="vab-name">' + name + '</td><td class="vab-value">' + value + '</td>';
    out = out + '</tr>\n';
    rowcnt++;
    return out;
},

renderIngredients: function( story ) {
    // TODO: insert new DOM objects instead of just writing raw html...
    var out = '';
    rowcnt = 0;
    out = out + '<h3 class="vab-header">Value Added</h3>\n';
    out = out + '<div class="vab-body">\n';
    out = out + '<table width="100%">\n';
    out = out + VAB.fmtRow( 'Article Title:', story.entryTitle );
    if( story.authorList.length > 0 ) {
        var author_html = '';
        for(var i=0; i < story.authorList.length; ++i) {
            var hc = story.authorList[i];
            author_html = author_html + VAB.renderHCard( hc );
        }
        out = out + VAB.fmtRow( 'Written by:', author_html );
    }
    if( story.published ) {
        out = out + VAB.fmtRow( 'Published:', story.published.toLocaleString() );
    }
    out = out + VAB.fmtRow( 'Last updated:', story.updated.toLocaleString() );
    if( story.principles ) {
        out = out + VAB.fmtRow( 'Statement of principles:', story.principles.name.link( story.principles.url ) );
    }

    out = out + '</table>\n';
    out = out + '</div>\n';

    return out;
},

renderHCard: function( hcard ) {
    var out = '';
    if( hcard.urlList ) {
        out = out + hcard.fn.link( hcard.urlList[0] );
    } else {
        out = out + hcard.fn;
    }
    out = out + "\n<br/>";
    return out;
},

addLoadEvent: function(func) {
  var oldonload = window.onload;
  if (typeof window.onload != 'function') {
    window.onload = func;
  } else {
    window.onload = function() {
      if (oldonload) {
        oldonload();
      }
      func();
    }
  }
}

}


VAB.addLoadEvent( VAB.go );

