/*
* File: jquery.barfiller.js
* Version: 1.0.1
* Description: A plugin that fills bars with a percentage you set.
* Author: 9bit Studios
* Copyright 2012, 9bit Studios
* http://www.9bitstudios.com
* Free to use and abuse under the MIT license.
* http://www.opensource.org/licenses/mit-license.php
*/

(function ($) {

    $.fn.barfiller = function (options) {

        var defaults = $.extend({
            barColor: '#16b597',
            tooltip: true,
            duration: 1000,
            animateOnResize: true,
            symbol: "%"
        }, options);


        /******************************
        Private Variables
        *******************************/         

        var object = $(this);
        var settings = $.extend(defaults, options);
        var barWidth = object.width();
        var fill = object.find('.fill');
        var toolTip = object.find('.tip');
        var fillPercentage = fill.attr('data-percentage');
        var resizeTimeout;
        var transitionSupport = false;
        var transitionPrefix;

        /******************************
        Public Methods
        *******************************/         
        
        var methods = {

            init: function() {
                return this.each(function () {
                    if(methods.getTransitionSupport()) {
                        transitionSupport = true;
                        transitionPrefix = methods.getTransitionPrefix();
                    }

                    methods.appendHTML();
                    methods.setEventHandlers();
                    methods.initializeItems();
                });
            },

            /******************************
            Append HTML
            *******************************/			

            appendHTML: function() {
                fill.css('background', settings.barColor);

                if(!settings.tooltip) {
                    toolTip.css('display', 'none');
                }
                toolTip.text(fillPercentage + settings.symbol);
            },
            

            /******************************
            Set Event Handlers
            *******************************/
            setEventHandlers: function() {
                if(settings.animateOnResize) {
                    $(window).on("resize", function(event){
                        clearTimeout(resizeTimeout);
                        resizeTimeout = setTimeout(function() { 
                        methods.refill(); 
                        }, 300);
                    });				
                }
            },				

            /******************************
            Initialize
            *******************************/			

            initializeItems: function() {
            var pctWidth = methods.calculateFill(fillPercentage);
            object.find('.tipWrap').css({ display: 'inline' });

            if(transitionSupport)
                methods.transitionFill(pctWidth);
            else
                methods.animateFill(pctWidth);
            },

            getTransitionSupport: function() {

                var thisBody = document.body || document.documentElement,
                thisStyle = thisBody.style;
                var support = thisStyle.transition !== undefined || thisStyle.WebkitTransition !== undefined || thisStyle.MozTransition !== undefined || thisStyle.MsTransition !== undefined || thisStyle.OTransition !== undefined;
                return support; 	
            },
                
            getTransitionPrefix: function() {
                if(/mozilla/.test(navigator.userAgent.toLowerCase()) && !/webkit/.test(navigator.userAgent.toLowerCase())) {
                    return '-moz-transition';
                }
                if(/webkit/.test(navigator.userAgent.toLowerCase())) {
                    return '-webkit-transition';
                }
                if(/opera/.test(navigator.userAgent.toLowerCase())) {
                    return '-o-transition';
                }
                if (/msie/.test(navigator.userAgent.toLowerCase())) {
                    return '-ms-transition';
                }
                else {
                    return 'transition';
                }
            },

            getTransition: function(val, time, type) {

                var CSSObj;
                if(type === 'width') {
                    CSSObj = { width : val };
                }
                else if (type === 'left') {
                    CSSObj = { left: val };
                }

                time = time/1000;
                CSSObj[transitionPrefix] = type+' '+time+'s ease-in-out';		    
                return CSSObj;

            },				

            refill: function() {
                fill.css('width', 0);
                toolTip.css('left', 0);
                barWidth = object.width();
                methods.initializeItems();
            },

            calculateFill: function(percentage) {
                percentage = percentage *  0.01;
                var finalWidth = barWidth * percentage;
                return finalWidth;
            },       

            transitionFill: function(barWidth) {

                var toolTipOffset = barWidth - toolTip.width();
                fill.css( methods.getTransition(barWidth, settings.duration, 'width'));
                toolTip.css( methods.getTransition(toolTipOffset, settings.duration, 'left'));

            },	

            animateFill: function(barWidth) {
                var toolTipOffset = barWidth - toolTip.width();
                fill.stop().animate({width: '+=' + barWidth}, settings.duration);
                toolTip.stop().animate({left: '+=' + toolTipOffset}, settings.duration);
            }
			
        };
        
        if (methods[options]) { 	// $("#element").pluginName('methodName', 'arg1', 'arg2');
            return methods[options].apply(this, Array.prototype.slice.call(arguments, 1));
        } else if (typeof options === 'object' || !options) { 	// $("#element").pluginName({ option: 1, option:2 });
            return methods.init.apply(this);  
        } else {
            $.error( 'Method "' +  method + '" does not exist in barfiller plugin!');
        } 
    };

})(jQuery);

/* jQuery Graph Plugin */
"use strict";var Graph=Graph||function(t){var i={};i.count=0;var e=function(t){0!==t&&(i.setOptions.call(this,t),++i.count)};return i.defaults=function(){return{x:["Sun","Mon","Tue","Wed","Thu","Fri","Sat"],y:10,attachTo:"body",points:[0,26,33,74,12,49,18]}},i.basics=function(e,s,o,a){e=o||e||300,s=a||s||550,e=e.toString(),s=s.toString(),i.attachTo=i.attachTo||"body";var n=t(i.attachTo).css("height"),r=t(i.attachTo).css("width");return e="%"===e.substring(e.length-1)?n:e,s="%"===s.substring(s.length-1)?r:s,{Gheight:parseFloat(e),Gwidth:parseFloat(s),xDist:60,yDist:30,scale:10,xOffset:25,yOffset:20,yStart:0,mainOffset:35,padding:10,xOfPoints:[],yOfPoints:[],mxOfPoints:[],myOfPoints:[],multipleDataSets:!1,legend:!1,interactive:!0,animations:!1,animationDuration:1,pointAnimation:!0,lineAnimation:!0,barAnimation:!0,pieAnimation:!0,grid:!0,xGrid:!0,yGrid:!0,xName:null,yName:null,special:null,showPoints:!0,noLines:!1,pointRadius:5,averagePointRadius:5,pieSize:200,tooltipWidth:50,pieLegend:!0,rx:10,before:"",after:"",title:"",id:"SVGGraph"+i.count}},i.parseS=function(t,i){return'svg[id="'+t+'"] '+i},i.id2selector=function(t){var i=t.split(" ");t=i[0];var e='svg[id="';if("#"!==t.charAt(0))return t;e+=t.substring(1)+'"]';for(var s=1,o=i.length;o>s;++s)e+=" "+i[s];return e},i.design=function(t){t.byCSS=t.byCSS||{},t.design=t.design||{};var i="bar"===t.type?"start":"middle",e=t.height||"100%",s=t.width||"100%",o=t.design,a={};a.style={},a.style[this.parseS(t.id,"")]={height:e,width:s},a.style[this.parseS(t.id,".grid")]={stroke:o.gridColor||"#000","stroke-width":o.gridWidth||"1"},a.style[this.parseS(t.id,".points")]={cursor:"pointer"},a.style[this.parseS(t.id,'circle:not(".middle"):not(".pie-tooltip")')]={opacity:.8},a.style[this.parseS(t.id,".inset")]={fill:o.pointColor||"lightblue"},a.style[this.parseS(t.id,".labels")]={fill:o.labelColor||"#000",stroke:o.labelStroke||"none","font-family":o.labelFont||"Arial","font-size":o.labelFontSize||"13px",kerning:o.labelKerning||"2"},a.style[this.parseS(t.id,".lines")]={stroke:o.lineColor||"darkgrey","stroke-width":o.lineWidth||"2"},a.style[this.parseS(t.id,".averageLine")]={stroke:o.averageLineColor||"green","stroke-width":o.lineWidth||"2"},a.style[this.parseS(t.id,".line-of-1")]={stroke:o.lineColor||"green","stroke-width":o.lineWidth||"2"},a.style[this.parseS(t.id,".rect")]={stroke:o.borderColor||"#fff","stroke-width":o.borderWidth||"2",fill:o.barColor||"blue",opacity:.8},a.style[this.parseS(t.id,".bar")]={stroke:o.barBorder||"#fff",opacity:.8},a.style[this.parseS(t.id,".SVG-tooltip")]={fill:o.tooltipColor||"#000","font-family":o.tooltipFont||"Arial","font-size":o.tooltipFontSize||"13px",display:"none",opacity:"1"},a.style[this.parseS(t.id,".SVG-tooltip-box")]={display:"none",fill:o.tooltipBoxColor||"none",stroke:o.borderColor||"none","stroke-width":o.borderWidth||"2"},a.style[this.parseS(t.id,".area")]={stroke:t.multipleDataSets?"none":o.lineColor||"green","stroke-width":o.borderWidth||"2",fill:o.areaColor||"none",opacity:.8},a.style[this.parseS(t.id,".middle")]={fill:o.donutCenterColor||"#fff"},a.style[this.parseS(t.id,".slice")]={stroke:o.borderColor||"grey","stroke-width":o.borderWidth||"2",opacity:"0.8"},a.style[this.parseS(t.id,".labels.x-labels")]={"text-anchor":o.xLabelAnchor||i},a.style[this.parseS(t.id,".labels.y-labels")]={"text-anchor":o.yLabelAnchor||"end"},a.style['table[id="'+t.id+'"]']={height:e,width:s,"border-collapse":"collapse","text-align":"center"};var n=t.colors||["red","blue","green","orange","purple","yellow","brown","gold","black","grey"];n.push("");for(var r=0,l=n.length;l>r;++r)a.style[this.parseS(t.id,".line-of-"+r)]={stroke:o.lineColor||n[r],"stroke-width":o.lineWidth||"2"},a.style[this.parseS(t.id,".path-of-"+r)]={fill:n[r],opacity:.8},a.style[this.parseS(t.id,".rect-of-"+r)]={fill:n[r]},a.style[this.parseS(t.id,".point-of-"+r)]={fill:n[r]};for(var p in t.byCSS)a.style[this.id2selector(p)]=t.byCSS[p];return a},i.setOptions=function(e){e=e||{},e.points&&t.isArray(e.points[0])&&(e.multipleDataSets=!0),e.attachTo&&(e.attachTo="#"===e.attachTo.charAt(0)?e.attachTo:"#"+e.attachTo,i.attachTo=e.attachTo),e.id&&(e.id="#"===e.id.charAt(0)?e.id.substring(1):e.id),(e.basic===!0||"undefined"==typeof e.basic)&&(this.obj=i.basics(e.height,e.width,e.graphHeight,e.graphWidth)),e&&e.example===!0||!t.isEmptyObject(e)?(e.id=e.id||this.obj.id,t.extend(this.obj,i.defaults(),e,i.design(e)),this.obj.addStyle=!0):e&&e.addStyle===!0?t.extend(this.obj,i.design(e),e):e&&(this.obj=e),this.obj.numPoints=this.obj.points.length,this.obj.xLength=this.obj.x.length},e.prototype.getData=function(){return JSON.stringify(this.obj)},e.prototype.genToFunc=function(t){return t="area"===t?"linear":"combo"===t?"bar":"donut"===t?"pie":t,"Graph"+t.charAt(0).toUpperCase()+t.substring(1)},e.prototype.expand=function(t,i){t="string"==typeof t?jQuery.parseJSON(t):t;var e=new(window[this.genToFunc(this.obj.type)])(t);i=i||"",e.init(i)},e.prototype.update=function(t){t=t||{},t.byCSS=this.obj.byCSS,this.expand(t,"update")},e.prototype.to=function(t,i){var e=i||this.obj;this.obj.type=t,e.type=t,this.expand(e,"update")},e.prototype.createGrid=function(t,i){var e=this.obj,s="",o="",a=e.yDist-30;if(e.grid&&!e.noLines){var n,r=e.height-i*e.yDist;if(e.xGrid)for(var l=0;t>l;++l)n=l*e.xDist+e.mainOffset,s+='<line x1="'+n+'" x2="'+n+'" y1="'+(e.height-e.yOffset-e.padding-a)+'" y2="'+r+'"></line>';var p=(t-1)*e.xDist+e.mainOffset;if(e.yGrid)for(var l=1;i>=l;++l)n=e.height-l*e.yDist,o+='<line x1="'+e.mainOffset+'" x2="'+p+'" y1="'+n+'" y2="'+n+'"></line>'}else e.noLines===!1&&(s+='<line x1="'+e.mainOffset+'" x2="'+e.mainOffset+'" y1="'+(e.height-e.yOffset-e.padding-a)+'" y2="'+(e.height-i*e.yDist)+'"></line>',o+='<line x1="'+e.mainOffset+'" x2="'+((t-1)*e.xDist+e.mainOffset)+'" y1="'+(e.height-e.yDist)+'" y2="'+(e.height-e.yDist)+'"></line>');return{xGrid:s,yGrid:o}},e.prototype.applyStyling=function(){var i=this.obj;if(i.addStyle)for(var e in i.style)t(e).css(i.style[e])},e.prototype.openTags=function(){return{SVG:'<svg id="'+this.obj.id+'"class="graph"style="'+(this.obj.css||"")+'">',xGrid:'<g class="grid x-grid" id="xGrid">',yGrid:'<g class="grid y-grid" id="yGrid">',xLabels:'<g class="labels x-labels">',yLabels:'<g class="labels y-labels">',title:'<g class="labels title">'}},e.prototype.addLabels=function(){for(var t=this.obj,i="",e="",s=0,o=t.xLength;o>s;++s)i+='<text x="'+(s*t.xDist+t.mainOffset)+'" y="'+(t.height-t.padding)+'">'+t.x[s]+"</text>";for(var s=1,o=t.y+1;o>=s;++s){var a=s*t.scale-t.scale+t.yStart,n=a>=10?t.xOffset:t.xOffset-10;e+='<text x="'+n+'" y="'+(t.height-(t.yDist*s-t.padding)-5)+'">'+a+"</text>"}return{xLabels:i,yLabels:e}},e.prototype.addTitle=function(t){var i=this.obj;return'<text x="'+i.mainOffset+'" y="'+(i.height-t*i.yDist-i.yOffset)+'"font-weight="bold">'+i.title+"</text>"},e.prototype.finishGraph=function(t,i,e,s){var o=this.obj;"pie"!==o.type&&(e.xGrid+=this.createGrid(t,i).xGrid,e.yGrid+=this.createGrid(t,i).yGrid,e.xLabels+=this.addLabels().xLabels,e.yLabels+=this.addLabels().yLabels),e.title+=this.addTitle(i),(o.legend&&o.pieLegend||"pie"===o.type)&&(e.legend=this.addLegend(s)),e.points=e.points||"";for(var a in e)e[a]!==e.points&&e[a]!==e.tooltips&&"SVG"!==a&&(e.SVG+=e[a]+"</g>");e.SVG+=e.points+e.tooltips+"</svg>";var n=o.before+e.SVG+o.after;return this.handleAppend(s,n),this.applyStyling(),e.SVG},e.prototype.handleAppend=function(i,e){"update"===i?t("#"+this.obj.id).replaceWith(e):t(this.obj.attachTo).append(e)},e.prototype.addLegend=function(){var i=this.obj,e=function(i){var e="add"===i?1:.8,s=t(this).attr("class").substring(7),o='[class*="'+s+'"][id^="'+t(this).attr("id").split("-")[1]+'"]';t("line"+o+", rect"+o+", path"+o).each(function(){t(this).css("opacity",e)})};i.interactive&&i.multipleDataSets&&(t(document).on("mouseover",'g[id^="legend-"]',function(){e.call(this,"add")}),t(document).on("mouseout",'g[id^="legend-"]',function(){e.call(this,"take")}));var s='<g class="legend">',o=i.legendX||i.Gwidth-i.xDist,a=30,n=30,r=i.yOffset;if(i.dataNames=i.dataNames||[],i.multipleDataSets||"pie"===i.type)for(var l=0,p=i.numPoints;p>l;++l)s+='<g id="legend-'+i.id+'"class="legend-of-'+l+'">',s+='<rect class="rect-of-'+l+'"x="'+o+'" y="'+r+'"width="'+a+'"height="'+n+'"></rect>',s+='<text style="cursor:default;"class="legend-of-'+l+'"x="'+(o+a+5)+'"y="'+(r+n/2)+'">'+(i.dataNames[l]||"Data"+(0===l?"":" "+l))+"</text>",r+=i.yDist+i.padding;else for(var l=0,p=i.xLength;p>l;++l)s+='<g id="legend-'+i.id+'">',s+='<text style="cursor:default;"x="'+1.5*o+'"y="'+(r+n/2)+'">'+(i.x[l]+" : "+i.points[l])+"</text>",r+=i.yDist+i.padding;return"combo"===i.special&&(s+='<g id="legend-avg-'+i.id+'">',s+='<rect fill="'+(i.design.averageLineColor||"green")+'"class="averageLine"x="'+o+'" y="'+r+'"width="'+a+'"height="'+n+'"></rect>',s+='<text style="cursor:default;"x="'+(o+a+5)+'"y="'+(r+n/2)+'">Average</text>'),s+="</g>"},e}(jQuery),GraphLinear=GraphLinear||function(t){var i=function(i){i=i||{},i.type="linear",Graph.call(this,i);var e=function(e){var s=t(this).attr("id"),o=s.split("-"),a=o[0],n=o[1],r=this;t('svg line[id^="'+a+'"], svg path[id^="'+a+'"]').each(function(){if(t(this).attr("id").split("-")[1]===n){var s="#"+t(r).attr("class").split(" ")[0]+"-tooltip",o="#"+t(r).attr("class").split(" ")[0]+"-tooltip-rect";"add"===e?(t(this).css("stroke-width",i.lineWidth||3),t(this).css("opacity",1),t(s).show(),t(o).show()):(t(this).css("stroke-width",i.lineWidth-1||2),t(this).css("opacity",.8),t(s).hide(),t(o).hide())}})};if(this.obj.interactive){var s=this;t(document).on("mouseover",'svg circle[id$="point"]',function(){e.call(this,"add"),t(this).css("opacity",1)}),t(document).on("mouseleave",'svg circle[id$="point"]',function(){e.call(this,"sub"),t(this).css("opacity",s.obj.style['svg[id="'+s.obj.id+'"] circle'].opacity||.8)})}};return i.prototype=Object.create(Graph.prototype),i.prototype.constructor=i,i.prototype.buildPoints=function(t,i){var e,s,o,a,n,r,l,p,d=i?this.obj.averagePointRadius:this.obj.pointRadius,h=this.obj,c=i||h.points;return 1===t.length?(o=c[t[0]],a=t[0],p=t[0],r=!1):2===t.length&&(o=c[t[0]][t[1]],a=""+t[0]+t[1],p=t[1],r=!0),e=h.height-(o+h.scale)*(h.yDist/h.scale),s=p*h.xDist+h.mainOffset,i&&(s+=h.xDist/(h.points.length+1)),l=r===!1?0:t[0],n='<circle id="'+h.id+"-"+l+'-point"class="'+h.id+"-point"+a+" "+(h.multipleDataSets&&!i?"point-of-"+t[0]+" ":"")+'"cx="'+s+'" cy="'+e+'" r="'+d+'">',!h.animations||!h.pointAnimation||h.multipleDataSets&&"area"===h.special||(n+='<animate attributeName="cy" from="0" to="'+e+'" dur="'+(h.animationDuration+p/7)+'s" fill="freeze">'),n+="</circle>",n+='<g><rect class="'+(h.multipleDataSets&&!i?"rect-of-"+t[0]+" ":"")+'SVG-tooltip-box"id="'+h.id+"-point"+a+'-tooltip-rect"rx="'+h.rx+'"x="'+(s-2*h.padding-h.tooltipWidth/2)+'"y="'+(e-h.yDist-2*h.padding)+'"height="'+(h.yDist+h.padding/2)+'"width="'+(50+h.tooltipWidth)+'"/>',n+='<text class="SVG-tooltip"id="'+h.id+"-point"+a+'-tooltip" x="'+(s-h.padding)+'" y="'+(e-h.yDist)+'">'+o+"</text></g>"},i.prototype.animateLines=function(){for(var i,e=this.obj,s=t("path[id^="+e.id+"]"),o=0,a=t("path[id^="+e.id+"]").length;a>o;++o)i=s[o].getTotalLength(),s[o].style.transition=s[o].style.WebkitTransition="none",s[o].style.strokeDasharray=i+" "+i,s[o].style.strokeDashoffset=i,s[o].getBoundingClientRect(),s[o].style.transition=s[o].style.WebkitTransition="stroke-dashoffset 2s ease-in-out",s[o].style.strokeDashoffset="0"},i.prototype.init=function(t){var i=this.obj;i.width=i.Gwidth,i.height=i.Gheight;var e=this.openTags();s||(e.lines='<g class="lines">'),e.points='<g class="inset points">';var s="area"===i.special;s&&!i.multipleDataSets&&(e.path='<g class="area"><path id="'+i.id+'-0-path"d="');var o,a,n,r=i.x.length,l=i.y+1,p=i.height-i.yDist;if(i.multipleDataSets){for(var d=0,h=i.numPoints;h>d;++d)i.mxOfPoints.push([]),i.myOfPoints.push([]);var c=[];e.path='<g class="area">';for(var d=0,h=i.numPoints;h>d;++d){for(var f=0,y=i.points[d].length;y>f;++f)o=i.height-(i.points[d][f]+i.scale)*(i.yDist/i.scale),a=f*i.xDist+i.mainOffset,i.showPoints===!0&&(e.points+=this.buildPoints([d,f])),i.mxOfPoints[d].push(a),i.myOfPoints[d].push(o);if(s){for(var f=0,y=i.points[d].length-1;y>f;++f)n=f+1,e.lines+='<line id="'+i.id+"-"+d+'-line" class="line-of-'+d+'" x1="'+i.mxOfPoints[d][f]+'" x2="'+i.mxOfPoints[d][n]+'" y1="'+i.myOfPoints[d][f]+'" y2="'+i.myOfPoints[d][n]+'"></line>';c.push('<path id="'+i.id+"-"+d+'-path"class="path-of-'+d+'" d="'),c[d]+="M"+i.mxOfPoints[d][0]+","+p+" ",c[d]+="L"+i.mxOfPoints[d][0]+","+i.myOfPoints[d][0]+" ";for(var f=0,y=i.points[d].length;y>f;++f)c[d]+="L"+i.mxOfPoints[d][f]+","+i.myOfPoints[d][f]+" ";c[d]+="L"+i.mxOfPoints[d][i.mxOfPoints[d].length-1]+","+p+'"></path>'}else{c.push('<path fill="none"id="'+i.id+"-"+d+'-path"class="line-of-'+d+'" d="'),c[d]+="M"+i.mxOfPoints[d][0]+","+i.myOfPoints[d][0]+" ";for(var f=0,y=i.points[d].length;y>f;++f)c[d]+="L"+i.mxOfPoints[d][f]+","+i.myOfPoints[d][f];c[d]+='"></path>'}}e.path+=c.join("")}else{for(var d=0;r>d;++d)o=i.height-(i.points[d]+i.scale)*(i.yDist/i.scale),a=d*i.xDist+i.mainOffset,i.showPoints===!0&&(e.points+=this.buildPoints([d])),i.xOfPoints.push(a),i.yOfPoints.push(o);if(s){e.path+="M"+i.xOfPoints[0]+","+p+" ",e.path+="L"+i.xOfPoints[0]+","+i.yOfPoints[0]+" ";for(var d=1;d<i.xOfPoints.length;++d)e.path+="L"+i.xOfPoints[d]+","+i.yOfPoints[d]+" ";e.path+="L"+i.xOfPoints[i.xOfPoints.length-1]+","+p+' "></path>'}else for(var d=0,h=i.numPoints-1;h>d;++d){e.lines+='<path fill="none"id="'+i.id+'-0-path"d="',e.lines+="M"+i.xOfPoints[0]+","+i.yOfPoints[0]+" ";for(var d=1;d<i.xOfPoints.length;++d)e.lines+="L"+i.xOfPoints[d]+","+i.yOfPoints[d];e.lines+='"</path>'}}this.finishGraph(r,l,e,t),i.multipleDataSets&&s||!i.animations||!i.lineAnimation||this.animateLines()},i}(jQuery),GraphBar=GraphBar||function(t){var i={},e=function(i){if(i=i||{},i.type="bar",Graph.call(this,i),this.obj.interactive){var e=this;t(document).on("mouseover","svg rect",function(){t("#"+t(this).attr("id")+"-tooltip").show(),t("#"+t(this).attr("id")+"-tooltip-rect").show(),t(this).css("opacity",1)}),t(document).on("mouseleave","svg rect",function(){t("#"+t(this).attr("id")+"-tooltip").hide(),t("#"+t(this).attr("id")+"-tooltip-rect").hide(),t(this).css("opacity",e.obj.style['svg[id="'+e.obj.id+'"] .rect'].opacity||.8)})}};return e.prototype=Object.create(Graph.prototype),e.prototype.constructor=e,i.getAveragePoints=function(t){for(var i,e=[],s=0,o=0,a=t[0].length;a>o;++o){i=0;for(var n=0,r=t.length;r>n;++n)i+=t[n][s];e.push(i/r),++s}return e},e.prototype.init=function(t){var e=this.obj;e.width=e.Gwidth,e.height=e.Gheight;var s=e.x.length+1,o=e.y+1,a=this.openTags();a.rects='<g class="rects"transform="translate(0, 40) scale(1, -1)">',a.tooltips="<g>";var n,r,l,p;if(p=e.yDist-30,e.multipleDataSets){for(var d=[],h=0,c=e.points[0].length;c>h;++h)d.push(0);e.points.push(d);var f,y,g=e.points.length,u=e.points[0].length,b=g-1,x=e.xDist/g,m=function(t){for(var i=0,s=0;u>s;++s){for(var o=0,d=g;d>o;++o)o!==b&&(f=o+i+s*b,y=o+i+2*s,n=0!==e.points[o][i]?(e.points[o][i]+e.scale)*(e.yDist/e.scale)-e.yDist:2,r=f*x+e.mainOffset,l=e.height-e.padding-e.yOffset-n,0===t?a.rects+='<rect class="rect-of-'+o+' bar"id="'+e.id+"-point-"+y+'" x="'+r+'" y="'+(-e.height+e.yDist+e.mainOffset+e.padding/2)+'" width="'+x+'"height="'+n+'"'+(e.animations&&e.barAnimation?'><animate attributeName="height" from="0" to="'+n+'" dur="'+e.animationDuration+'s" fill="freeze"></animate></rect>':"/>"):1===t&&(a.tooltips+='<g><rect class="rect-of-'+o+' SVG-tooltip-box "id="'+e.id+"-point-"+y+'-tooltip-rect"rx="'+e.rx+'"x="'+(r-e.tooltipWidth/2)+'"y="'+(l-p-e.yDist-2*e.padding)+'"height="'+(e.yDist+e.padding/2+10)+'"width="'+(x+e.tooltipWidth)+'"/>',a.tooltips+='<text class="SVG-tooltip"id="'+e.id+"-point-"+y+'-tooltip" x="'+(r+x/2-e.padding)+'" y="'+(l-p-e.yDist/2-e.padding)+'">'+e.points[o][i]+"</text></g>"));e.xOfPoints.length<u&&e.xOfPoints.push(r),++i}};if(m(0),m(1),e.points.pop(),"combo"===e.special){var v=i.getAveragePoints(e.points),S=new GraphLinear(e);a.lines='<g class="lines">',a.points='<g class="inset points">';for(var h=0,c=s-1;c>h;++h)n=e.height-(v[h]+e.scale)*(e.yDist/e.scale),r=h*e.xDist+e.mainOffset,e.showPoints===!0&&(a.points+=S.buildPoints([h],v)),e.yOfPoints.push(n);for(var h=0,c=v.length-1;c>h;++h){a.lines+='<path class="averageLine"fill="none"id="'+e.id+'-0-path"d="',a.lines+="M"+e.xOfPoints[0]+","+e.yOfPoints[0]+" ";for(var h=1;h<e.xOfPoints.length;++h)a.lines+="L"+e.xOfPoints[h]+","+e.yOfPoints[h];a.lines+='"</path>'}}}else{for(var h=0,c=s-1;c>h;++h)n=0!==e.points[h]?(e.points[h]+e.scale)*(e.yDist/e.scale)-e.yDist:2,r=h*e.xDist+e.mainOffset,a.rects+='<rect class="rect bar"id="'+e.id+"-point-"+h+'" x="'+r+'" y="'+(-e.height+e.yDist+e.mainOffset+e.padding/2)+'" width="'+e.xDist+'"height="'+n+'"'+(e.animations===!0?'><animate attributeName="height" from="0" to="'+n+'" dur="'+e.animationDuration+'s" fill="freeze"></animate></rect>':"/>");for(var h=0,c=s-1;c>h;++h)n=0!==e.points[h]?(e.points[h]+e.scale)*(e.yDist/e.scale)-e.yDist:2,r=h*e.xDist+e.mainOffset,l=e.height-e.padding-e.yOffset-n,a.tooltips+='<rect class="SVG-tooltip-box"id="'+e.id+"-point-"+h+'-tooltip-rect"rx="'+e.rx+'"x="'+(r+e.padding/2-e.tooltipWidth/2)+'"y="'+(l-p-e.yDist-2*e.padding)+'"height="'+(e.yDist+e.padding/2)+'"width="'+(e.xDist-e.padding+e.tooltipWidth)+'"/>',a.tooltips+='<text class="SVG-tooltip"id="'+e.id+"-point-"+h+'-tooltip" x="'+(r+e.xDist/2-e.padding)+'" y="'+(l-p-e.yDist/2-e.padding)+'">'+e.points[h]+"</text>"}this.finishGraph(s,o,a,t),"combo"===e.special&&e.multipleDataSets&&e.animations&&S.animateLines()},e}(jQuery),GraphTable=GraphTable||function(){var t=function(t){t=t||{},t.type="table",Graph.call(this,t)};return t.prototype=Object.create(Graph.prototype),t.prototype.constructor=t,t.prototype.init=function(t){var i=this.obj,e="<th>"+(i.dataNames?i.dataNames[0]:"Data")+"</th>",s="<tr>";if(i.multipleDataSets)for(var o,a=0,n=i.xLength;n>a;++a){a<i.numPoints-1&&(e+="<th>"+i.dataNames[a+1]+"</th>"),o="";for(var r=0,l=i.numPoints;l>r;++r)o+="<td>"+i.points[r][a]+"</td>";s+="<td>"+a+"</td><td>"+i.x[a]+"</td>"+o+"</tr><tr>"}else for(var a=0,n=i.xLength;n>a;++a)s+="<td>"+a+"</td><td>"+i.x[a]+"</td><td>"+i.points[a]+"</td></tr><tr>";var p='<table class="SVG-table"id="'+i.id+'" border="1"cellpadding="5"><tr><th>#</th><th>'+(i.xName||"X")+"</th>"+e+"</tr>";p+=s+"</tr>",this.handleAppend(t,p),this.applyStyling()},t}(),GraphPie=GraphPie||function(t){var i={},e=function(i){if(i=i||{},i.type="pie",Graph.call(this,i),this.obj.interactive){var e=this.obj;t(document).on("mouseover",'svg path[id^="'+e.id+'"].slice',function(){t("#"+e.id+" .SVG-tooltip").hide(),t("#"+e.id+" .SVG-tooltip-title").hide(),t("#"+t(this).attr("id")+"-tooltip").show(),t("#"+t(this).attr("id")+"-tooltip-title").show(),t('svg path[id^="'+e.id+'"].slice').css("opacity",.8),t('svg path[id^="'+e.id+'"].slice').css("stroke",self.borderColor||"grey"),t(this).css("opacity",1),t(this).css("stroke","#000")}),t(document).on("mouseleave",'svg path[id^="'+e.id+'"].slice',function(){})}};return e.prototype=Object.create(Graph.prototype),e.prototype.constructor=e,i.lineTo=function(t,i){return"L"+t+","+i},i.percent=function(t){return Math.round(100*t)+"%"},e.prototype.init=function(e){if(!this.obj.multipleDataSets){var s=this.obj,o=this.openTags();o.pie='<g class="paths">';var a,n,r,l,p,d,h=0,c=s.pieSize||200,f=c-20,y="M"+c+","+c,g="A"+f+","+f,u="0 0,1",b=20,x=i.lineTo(b,c),m=0;s.dataNames=s.x.slice(0);for(var v=0,S=s.numPoints;S>v;++v)h+=s.points[v];for(var v=0,S=s.numPoints;S>v;++v)0!==v&&(x=i.lineTo(a,n)),m+=s.points[v]/h,r=2*m*Math.PI,l=Math.sin(r),p=Math.cos(r),a=c-f*p,n=c-f*l,0===v&&(d=y+x+g+" "+u+a+","+n),o.pie+='<path title="'+s.points[v]+" ("+i.percent(s.points[v]/h)+')"id="'+s.id+"-point-"+v+'"class="path-of-'+v+' slice" d="'+y+x+g+" "+u+a+","+n+'Z">',o.pie+="</path>";o.tooltips+='<g><circle class="pie-tooltip"id="'+s.id+"-point-"+v+'-tooltip-rect"style="fill:'+(s.design.pieTooltipFill||"#fff")+";opacity:"+(s.design.pieTooltipOpacity||.5)+'"r="'+(s.design.pieTooltipRadius||60)+'"cx="'+c+'"cy="'+c+'"height="'+(s.design.donutCenterRadius||c/2)+'"width="'+(s.design.donutCenterRadius||c/2)+'"/>';for(var O=c-c/4,D="",v=0;S>v;++v)D=s.points[v]+" ("+i.percent(s.points[v]/h)+")",o.tooltips+='<text class="SVG-tooltip"id="'+s.id+"-point-"+v+'-tooltip" x="'+(s.design.pieTooltipTextX||c-20*D.length/4)+'" y="'+(O+c/4+b)+'">'+D+")</text>",o.tooltips+='<text class="SVG-tooltip-title"style="display:none;font-weight:bold;font-size:25px;"id="'+s.id+"-point-"+v+'-tooltip-title" x="'+(s.design.pieTooltipTitleX||c-25*s.dataNames[v].toString().length/4)+'" y="'+(O+c/8)+'">'+s.dataNames[v]+"</text></g>";if("donut"===s.special&&(o.middle='<g><circle class="middle"cx="'+c+'" cy="'+c+'" r="'+(s.design.donutCenterRadius||c/2)+'"/>'),s.dataNames)for(var v=0,S=s.dataNames.length;S>v;++v)s.dataNames[v]+=" : "+s.points[v]+" ("+i.percent(s.points[v]/h)+")";this.finishGraph(0,0,o,e),t('svg path[id^="'+s.id+'"].slice').eq(2).mouseover()}},e}(jQuery);!function(t){t.fn.graphify=t.fn.graphify||function(i){i=i||{};var e,s,o,a=t.extend({height:this.css("height"),width:this.css("width"),start:"linear",pos:"top",obj:{}},i),n=a.obj,r=n.id,l=new Graph(0),p={};e=t.isArray(n.points[0])?["linear","area","bar","combo","table"]:["linear","area","bar","pie","donut","table"];var d=this.attr("id")+"-wrapper";this.append('<div id="'+d+'"><div id="'+d+'-g-area"></div></div>'),n.attachTo=d+"-g-area";var h=function(){for(var t="",i=0,s=e.length;s>i;++i)t+='<button id="'+r+"-graphify-button-"+e[i]+'">'+e[i].charAt(0).toUpperCase()+e[i].substring(1)+"</button>&emsp;";return t}();"top"===a.pos&&t("#"+d).prepend(h+"<br/><br />");var c=a.start;"area"!==c&&"combo"!==c&&"donut"!==c?s=new(window[l.genToFunc(c)])(n):(n.special=c,s=new(window[l.genToFunc(c)])(n)),s.init(),"bottom"===a.pos&&this.append(h),t(document).on("click",'button[id^="'+r+'-graphify-button-"]',function(){var i=t(this).attr("id").split("-")[3];if(p.hasOwnProperty(i)&&!n.animations)t("#"+d+"-g-area").html(p[i]);else{if("area"!==i&&"combo"!==i&&"donut"!==i)n.special=!1,s.to(i,n);else switch(n.special=i,i){case"area":s.to("linear",n);break;case"combo":s.to("bar",n);break;case"donut":s.to("pie",n)}o=new XMLSerializer,p[i]=o.serializeToString(document.getElementById(n.id))}n.type=i})}}(jQuery);
