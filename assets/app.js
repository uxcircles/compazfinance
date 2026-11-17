(function () {
  "use strict";
  var zh = document.documentElement.lang.indexOf("zh") === 0;

  /* ---------- menu ---------- */
  var mb = document.querySelector(".menu-btn"), nav = document.getElementById("nav");
  if (mb && nav) {
    mb.addEventListener("click", function () {
      var open = nav.classList.toggle("open");
      mb.setAttribute("aria-expanded", open);
      document.body.classList.toggle("menu-open", open);
    });
    nav.addEventListener("click", function (e) {
      if (e.target.tagName === "A") { nav.classList.remove("open"); document.body.classList.remove("menu-open"); mb.setAttribute("aria-expanded", "false"); }
    });
  }

  /* ---------- helpers ---------- */
  var gbp = new Intl.NumberFormat("en-GB", { style: "currency", currency: "GBP", maximumFractionDigits: 0 });
  function $(id) { return document.getElementById(id); }
  function num(id) { var v = parseFloat($(id).value); return isFinite(v) && v >= 0 ? v : 0; }
  function set(id, t) { var el = $(id); if (el) el.textContent = t; }
  function pct(v) { return (Math.round(v * 10) / 10) + "%"; }
  function repay(P, ratePct, years) {
    var n = Math.round(years * 12), r = ratePct / 100 / 12;
    if (P <= 0 || n <= 0) return 0;
    if (r === 0) return P / n;
    return P * r / (1 - Math.pow(1 + r, -n));
  }
  // SDLT, England & NI, residential rates from 1 April 2025 (GOV.UK)
  function bands(price, list) {
    var tax = 0, prev = 0;
    for (var i = 0; i < list.length; i++) {
      var top = list[i][0], rate = list[i][1];
      if (price > prev) tax += (Math.min(price, top) - prev) * rate;
      prev = top;
    }
    return Math.round(tax);
  }
  var STD = [[125000, 0], [250000, .02], [925000, .05], [1500000, .10], [Infinity, .12]];
  function sdlt(price, opts) {
    opts = opts || {};
    if (opts.ftb && price <= 500000) return bands(price, [[300000, 0], [500000, .05]]) + (opts.nr ? Math.round(price * .02) : 0);
    var extra = (opts.additional ? .05 : 0) + (opts.nr ? .02 : 0);
    var list = STD.map(function (b) { return [b[0], b[1] + extra]; });
    if (opts.additional && price < 40000) return 0;
    return bands(price, list);
  }

  /* ---------- compass tool ---------- */
  var tool = $("tool");
  if (tool) {
    var current = "buy";
    var needle = $("needle");
    var cta = $("tool-cta");
    var ctaBase = cta.getAttribute("href");
    var labels = {
      buy: zh ? "首套房或换房" : "First home or moving",
      remo: zh ? "转贷" : "Remortgage",
      btl: zh ? "买房出租" : "Buy-to-let",
      bridge: zh ? "过桥贷款" : "Bridging loan"
    };
    var summary = "";

    var calc = {
      buy: function () {
        var price = num("b-price"), dep = Math.min(num("b-dep"), price), loan = price - dep;
        var m = repay(loan, num("b-rate"), num("b-term"));
        var ftb = $("b-ftb").checked;
        var tax = sdlt(price, { ftb: ftb });
        set("buy-big", gbp.format(m));
        set("buy-o0", gbp.format(loan));
        set("buy-o1", price ? pct(loan / price * 100) : "–");
        set("buy-o2", gbp.format(tax));
        summary = (zh ? "房价 " : "Price ") + gbp.format(price) + ", " + (zh ? "首付 " : "deposit ") + gbp.format(dep) +
          ", " + num("b-rate") + "%, " + num("b-term") + (zh ? " 年" : " years") + (ftb ? (zh ? "，首次购房" : ", first-time buyer") : "") +
          " → ≈ " + gbp.format(m) + (zh ? "/月" : "/month");
      },
      remo: function () {
        var bal = num("r-bal"), yrs = num("r-term");
        var a = repay(bal, num("r-now"), yrs), b = repay(bal, num("r-new"), yrs), d = a - b;
        set("remo-big", gbp.format(Math.max(d, 0)));
        set("remo-o0", gbp.format(a));
        set("remo-o1", gbp.format(b));
        set("remo-o2", gbp.format(Math.max(d, 0) * 12));
        summary = (zh ? "剩余贷款 " : "Balance ") + gbp.format(bal) + ", " + yrs + (zh ? " 年" : " years") + ", " + num("r-now") + "% → " + num("r-new") + "%";
      },
      btl: function () {
        var price = num("l-price"), dep = Math.min(num("l-dep"), price), loan = price - dep, rent = num("l-rent");
        var interest = loan * num("l-rate") / 100 / 12;
        var nr = $("l-nr").checked;
        set("btl-big", gbp.format(interest));
        set("btl-o0", interest > 0 ? Math.round(rent / interest * 100) + "%" : "–");
        set("btl-o1", price ? pct(loan / price * 100) : "–");
        set("btl-o2", gbp.format(sdlt(price, { additional: true, nr: nr })));
        summary = (zh ? "房价 " : "Price ") + gbp.format(price) + ", " + (zh ? "首付 " : "deposit ") + gbp.format(dep) + ", " + (zh ? "月租 " : "rent ") + gbp.format(rent) + "/" + (zh ? "月" : "month") + (nr ? (zh ? "，非英国居民" : ", non-UK resident") : "");
      },
      bridge: function () {
        var loan = num("g-loan"), months = num("g-months");
        var interest = loan * num("g-rate") / 100 * months;
        var fee = loan * num("g-fee") / 100;
        set("bridge-big", gbp.format(interest + fee));
        set("bridge-o0", gbp.format(interest));
        set("bridge-o1", gbp.format(fee));
        set("bridge-o2", gbp.format(loan + interest + fee));
        summary = (zh ? "借款 " : "Borrow ") + gbp.format(loan) + ", " + months + (zh ? " 个月" : " months") + ", " + num("g-rate") + (zh ? "%/月" : "% a month");
      }
    };

    function run() {
      calc[current]();
      var q = "?about=" + current + "&note=" + encodeURIComponent(summary);
      cta.setAttribute("href", ctaBase + q);
    }

    function select(b, focus) {
      if (!calc[b]) return;
      current = b;
      tool.querySelectorAll(".bearings button").forEach(function (btn) {
        var on = btn.getAttribute("data-b") === b;
        btn.setAttribute("aria-pressed", on);
        if (on) {
          var deg = +btn.getAttribute("data-deg");
          needle.style.transform = "rotate(" + deg + "deg)";
          tool.querySelectorAll(".dial text").forEach(function (t) { t.classList.toggle("on", +t.getAttribute("data-deg") === deg); });
        }
      });
      tool.querySelectorAll("[data-panel]").forEach(function (p) { p.hidden = p.getAttribute("data-panel") !== b; });
      run();
      if (focus) { var f = tool.querySelector('fieldset[data-panel="' + b + '"] input'); if (f) f.focus({ preventScroll: true }); }
    }

    tool.querySelectorAll(".bearings button").forEach(function (btn) {
      btn.addEventListener("click", function () { select(btn.getAttribute("data-b")); });
    });
    tool.addEventListener("input", run);
    tool.addEventListener("change", run);

    var start = new URLSearchParams(location.search).get("b");
    select(calc[start] ? start : "buy");
  }

  /* ---------- enquiry form ---------- */
  var form = $("enquiry");
  if (form) {
    var p = new URLSearchParams(location.search);
    if (p.get("about") && form.topic.querySelector('option[value="' + p.get("about") + '"]')) form.topic.value = p.get("about");
    if (p.get("note")) form.message.value = (zh ? "我用网站计算器估算了：" : "I tried the estimate on your website: ") + p.get("note") + "\n\n";

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var ok = true;
      function check(el, valid) {
        el.closest("div").classList.toggle("bad", !valid);
        if (!valid && ok) { el.focus(); ok = false; }
      }
      check(form.name, form.name.value.trim().length > 1);
      check(form.email, /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email.value.trim()));
      check($("f-ok"), $("f-ok").checked);
      if (!ok) return;
      var topic = form.topic.options[form.topic.selectedIndex].text;
      var body = (zh ? "姓名：" : "Name: ") + form.name.value.trim() + "\n" +
        (zh ? "电邮：" : "Email: ") + form.email.value.trim() + "\n" +
        (form.phone.value.trim() ? (zh ? "手机：" : "Mobile: ") + form.phone.value.trim() + "\n" : "") +
        (zh ? "咨询内容：" : "About: ") + topic + "\n\n" + form.message.value.trim();
      location.href = "mailto:info@compazfinance.co.uk?subject=" + encodeURIComponent((zh ? "网站咨询：" : "Website enquiry: ") + topic) + "&body=" + encodeURIComponent(body);
    });
  }
})();
