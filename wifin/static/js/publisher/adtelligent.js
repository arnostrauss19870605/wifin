!(function() {
    window.googletag = window.googletag || {};
    window.vmpbjs = window.vmpbjs || {};
    window.vpb = window.vpb || {};
    vpb.cmd = vpb.cmd || [];
    vpb.st = Date.now();
    vpb.fastLoad = true;
    googletag.cmd = googletag.cmd || [];
    vmpbjs.cmd = vmpbjs.cmd || [];
    var cmds = [];
    try {
        cmds = googletag.cmd.slice(0);
        googletag.cmd.length = 0;
    } catch (e) {}
    var ready = false;

    function exec(cb) {
        return cb.call(googletag);
    }
    var overriden = false;
    googletag.cmd.push(function() {
        overriden = true;
        googletag.cmd.unshift = function(cb) {
            if (ready) {
                return exec(cb);
            }
            cmds.unshift(cb);
            if (cb._startgpt) {
                ready = true;
                for (var k = 0; k < cmds.length; k++) {
                    exec(cmds[k]);
                }
            }
        };
        googletag.cmd.push = function(cb) {
            if (ready) {
                return exec(cb);
            }
            cmds.push(cb);
        };
    });
    if (!overriden) {
        googletag.cmd.push = function(cb) {
            cmds.push(cb);
        };
        googletag.cmd.unshift = function(cb) {
            cmds.unshift(cb);
            if (cb._startgpt) {
                ready = true;
                if (googletag.apiReady) {
                    cmds.forEach(function(cb) {
                        googletag.cmd.push(cb);
                    });
                } else {
                    googletag.cmd = cmds;
                }
            }
        };
    }
    var dayMs = 36e5,
        cb = Math.floor(Date.now() * Math.random()),
        vpbSrc = 'https://protect-za.mimecast.com/s/Z6DvCmwVyvFl3TVN4ee' + cb + '/wrapper_hb_750279_18298.js',
        pbSrc = vpbSrc.replace('wrapper_hb', 'hb'),
        gptSrc = 'https://protect-za.mimecast.com/s/yggYCnZVOwiD2C4hgdV',
        c = document.head || document.body || document.documentElement;

    function loadScript(src, cb) {
        var s = document.createElement('script');
        s.src = src;
        s.defer = false;
        c.appendChild(s);
        s.onload = cb;
        s.onerror = function() {
            var fn = function() {};
            fn._startgpt = true;
            googletag.cmd.unshift(fn);
        };
        return s;
    }
    loadScript(pbSrc);
    loadScript(gptSrc);
    loadScript(vpbSrc);
})()