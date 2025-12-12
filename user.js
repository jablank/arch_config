/****************************************************************************************
 * Fastfox                                                                              *
 * "Non ducor duco"                                                                     *
 * priority: speedy browsing                                                            *
 * version: 144                                                                         *
 * url: https://github.com/yokoffing/Betterfox                                          *
 ***************************************************************************************/

/****************************************************************************
 * SECTION: GENERAL                                                        *
****************************************************************************/

// PREF: initial paint delay
// How long FF will wait before rendering the page (in ms)
// [NOTE] You may prefer using 250.
// [NOTE] Dark Reader users may want to use 1000 [3].
// [1] https://bugzilla.mozilla.org/show_bug.cgi?id=1283302
// [2] https://docs.google.com/document/d/1BvCoZzk2_rNZx3u9ESPoFjSADRI0zIPeJRXFLwWXx_4/edit#heading=h.28ki6m8dg30z
// [3] https://old.reddit.com/r/firefox/comments/o0xl1q/reducing_cpu_usage_of_dark_reader_extension/
// [4] https://reddit.com/r/browsers/s/wvNB7UVCpx
//user_pref("nglayout.initialpaint.delay", 5); // DEFAULT; formerly 250
    //user_pref("nglayout.initialpaint.delay_in_oopif", 5); // DEFAULT

// PREF: Font rendering cache in Skia (32MB)
// Increases font cache size to improve performance on text-heavy websites.
// Especially beneficial for sites with many font faces or complex typography.
// [1] https://bugzilla.mozilla.org/show_bug.cgi?id=1239151#c2
user_pref("gfx.content.skia-font-cache-size", 32); // 32 MB; default=5; Chrome=20


// PREF: GPU-accelerated Canvas2D
// Uses Accelerated Canvas2D for hardware acceleration of Canvas2D.
// This provides a consistent acceleration architecture across all platforms
// by utilizing WebGL instead of relying upon Direct2D.
// [WARNING] May cause issues on some Windows machines using integrated GPUs [2] [3]
// Add to your overrides if you have a dedicated GPU.
// [NOTE] Higher values will use more memory.
// [1] https://bugzilla.mozilla.org/show_bug.cgi?id=1741501
// [2] https://github.com/yokoffing/Betterfox/issues/153
// [3] https://github.com/yokoffing/Betterfox/issues/198
//user_pref("gfx.canvas.accelerated", true); // [DEFAULT FF133+]
user_pref("gfx.canvas.accelerated.cache-items", 32768); // [default=8192 FF135+]; Chrome=4096
user_pref("gfx.canvas.accelerated.cache-size", 4096); // default=256; Chrome=512
//user_pref("gfx.canvas.max-size", 32767); // DEFAULT=32767

// PREF: WebGL
user_pref("webgl.max-size", 16384); // default=1024
//user_pref("webgl.force-enabled", true);

// PREF: prefer GPU over CPU
// At best, the prefs do nothing on Linux/macOS.
// At worst, it'll result in crashes if the sandboxing is a WIP.
// [1] https://firefox-source-docs.mozilla.org/dom/ipc/process_model.html#gpu-process
//user_pref("layers.gpu-process.enabled", true); // DEFAULT WINDOWS
    //user_pref("layers.gpu-process.force-enabled", true); // enforce
    //user_pref("layers.mlgpu.enabled", true); // LINUX
//user_pref("media.hardware-video-decoding.enabled", true); // DEFAULT WINDOWS macOS
    //user_pref("media.hardware-video-decoding.force-enabled", true); // enforce
//user_pref("media.gpu-process-decoder", true); // DEFAULT WINDOWS
//user_pref("media.ffmpeg.vaapi.enabled", true); // LINUX

// PREF: hardware and software decoded video overlay [FF116+]
// [1] https://bugzilla.mozilla.org/show_bug.cgi?id=1829063
// [2] https://phabricator.services.mozilla.com/D175993
//user_pref("gfx.webrender.dcomp-video-hw-overlay-win", true); // DEFAULT
    //user_pref("gfx.webrender.dcomp-video-hw-overlay-win-force-enabled", true); // enforce
//user_pref("gfx.webrender.dcomp-video-sw-overlay-win", true); // DEFAULT
    //user_pref("gfx.webrender.dcomp-video-sw-overlay-win-force-enabled", true); // enforce

/****************************************************************************
 * SECTION: IMAGE CACHE                                                     *
****************************************************************************/

// PREF: image cache
user_pref("image.cache.size", 10485760); // (cache images up to 10MiB in size) [DEFAULT 5242880]
user_pref("image.mem.decode_bytes_at_a_time", 65536); // default=16384; alt=32768; chunk size for calls to the image decoders
//user_pref("image.mem.max_decoded_image_kb", 512000); // 500MB [HIDDEN OR REMOVED?]

// PREF: set minimum timeout to unmap shared surfaces since they have been last used
// [NOTE] This is only used on 32-bit builds of Firefox where there is meaningful
// virtual address space pressure.
// [1] https://phabricator.services.mozilla.com/D109440
// [2] https://bugzilla.mozilla.org/show_bug.cgi?id=1699224
//user_pref("image.mem.shared.unmap.min_expiration_ms", 120000); // default=60000; minimum timeout to unmap shared surfaces since they have been last used

/****************************************************************************
 * SECTION: NETWORK                                                         *
****************************************************************************/

// PREF: use bigger packets
// [WARNING] Cannot open HTML files bigger than 4MB if value is too large [2].
// Reduce Firefox's CPU usage by requiring fewer application-to-driver data transfers.
// However, it does not affect the actual packet sizes transmitted over the network.
// [1] https://www.mail-archive.com/support-seamonkey@lists.mozilla.org/msg74561.html
// [2] https://github.com/yokoffing/Betterfox/issues/279
// [3] https://ra1ahq.blog/en/optimizaciya-proizvoditelnosti-mozilla-firefox
//user_pref("network.buffer.cache.size", 65535); // default=32768 (32 kb); 262144 too large
//user_pref("network.buffer.cache.count", 48); // default=24; 128 too large

// PREF: increase the absolute number of HTTP connections
// [1] https://kb.mozillazine.org/Network.http.max-connections
// [2] https://kb.mozillazine.org/Network.http.max-persistent-connections-per-server
// [3] https://www.reddit.com/r/firefox/comments/11m2yuh/how_do_i_make_firefox_use_more_of_my_900_megabit/jbfmru6/
user_pref("network.http.max-connections", 1800); // default=900
user_pref("network.http.max-persistent-connections-per-server", 10); // default=6; download connections; anything above 10 is excessive
    user_pref("network.http.max-urgent-start-excessive-connections-per-host", 5); // default=3
    //user_pref("network.http.max-persistent-connections-per-proxy", 48); // default=32
user_pref("network.http.request.max-start-delay", 5); // default=10
//user_pref("network.websocket.max-connections", 200); // DEFAULT

// PREF: pacing requests [FF23+]
// Controls how many HTTP requests are sent at a time.
// Pacing HTTP requests can have some benefits, such as reducing network congestion,
// improving web page loading speed, and avoiding server overload.
// Pacing requests adds a slight delay between requests to throttle them.
// If you have a fast machine and internet connection, disabling pacing
// may provide a small speed boost when loading pages with lots of requests.
// false = Firefox will send as many requests as possible without pacing
// true = Firefox will pace requests (default)
user_pref("network.http.pacing.requests.enabled", false);
    //user_pref("network.http.pacing.requests.min-parallelism", 10); // default=6
    //user_pref("network.http.pacing.requests.burst", 32); // default=10

// PREF: increase DNS cache
// [1] https://developer.mozilla.org/en-US/docs/Web/Performance/Understanding_latency
user_pref("network.dnsCacheEntries", 10000); // default=800

// PREF: adjust DNS expiration time
// [ABOUT] about:networking#dns
// [NOTE] These prefs will be ignored by DNS resolver if using DoH/TRR.
user_pref("network.dnsCacheExpiration", 3600); // keep entries for 1 hour; default=60
    //user_pref("network.dnsCacheExpirationGracePeriod", 120); // default=60; cache DNS entries for 2 minutes after they expire

// PREF: the number of threads for DNS
//user_pref("network.dns.max_high_priority_threads", 40); // DEFAULT [FF 123?]
//user_pref("network.dns.max_any_priority_threads", 24); // DEFAULT [FF 123?]

// PREF: increase TLS token caching 
user_pref("network.ssl_tokens_cache_capacity", 10240); // default=2048; more TLS token caching (fast reconnects)

// PREF: link-mouseover opening connection to linked server
// When accessing content online, devices use sockets as endpoints.
// The global limit on half-open sockets controls how many speculative
// connection attempts can occur at once when starting new connections [3].
// If the user follows through, pages can load faster since some
// work was done in advance. Firefox opens predictive connections
// to sites when hovering over New Tab thumbnails or starting a
// URL Bar search [1] and hyperlinks within a page [2].
// [NOTE] DNS (if enabled), TCP, and SSL handshakes are set up in advance,
// but page contents are not downloaded until a click on the link is registered.
// [1] https://support.mozilla.org/en-US/kb/how-stop-firefox-making-automatic-connections?redirectslug=how-stop-firefox-automatically-making-connections&redirectlocale=en-US#:~:text=Speculative%20pre%2Dconnections
// [2] https://news.slashdot.org/story/15/08/14/2321202/how-to-quash-firefoxs-silent-requests
// [3] https://searchfox.org/mozilla-central/rev/028c68d5f32df54bca4cf96376f79e48dfafdf08/modules/libpref/init/all.js#1280-1282
// [4] https://www.keycdn.com/blog/resource-hints#prefetch
// [5] https://3perf.com/blog/link-rels/#prefetch
user_pref("network.http.speculative-parallel-limit", 0);

// PREF: DNS prefetching for HTMLLinkElement <link rel="dns-prefetch">
// Used for cross-origin connections to provide small performance improvements.
// You can enable rel=dns-prefetch for the HTTPS document without prefetching
// DNS for anchors, whereas the latter makes more specualtive requests [5].
// [1] https://bitsup.blogspot.com/2008/11/dns-prefetching-for-firefox.html
// [2] https://css-tricks.com/prefetching-preloading-prebrowsing/#dns-prefetching
// [3] https://www.keycdn.com/blog/resource-hints#2-dns-prefetching
// [4] http://www.mecs-press.org/ijieeb/ijieeb-v7-n5/IJIEEB-V7-N5-2.pdf
// [5] https://bugzilla.mozilla.org/show_bug.cgi?id=1596935#c28
user_pref("network.dns.disablePrefetch", true);
    user_pref("network.dns.disablePrefetchFromHTTPS", true); // [FF127+ false]

// PREF: DNS prefetch for HTMLAnchorElement (speculative DNS)
// Disable speculative DNS calls to prevent Firefox from resolving
// hostnames for other domains linked on a page. This may eliminate
// unnecessary DNS lookups, but can increase latency when following external links.
// [1] https://bugzilla.mozilla.org/show_bug.cgi?id=1596935#c28
// [2] https://github.com/arkenfox/user.js/issues/1870#issuecomment-2220773972
//user_pref("dom.prefetch_dns_for_anchor_http_document", false); // [FF128+]
//user_pref("dom.prefetch_dns_for_anchor_https_document", false); // DEFAULT [FF128+]

// PREF: enable <link rel="preconnect"> tag and Link: rel=preconnect response header handling
//user_pref("network.preconnect", true); // DEFAULT

// PREF: preconnect to the autocomplete URL in the address bar
// Whether to warm up network connections for autofill or search results.
// Firefox preloads URLs that autocomplete when a user types into the address bar.
// Connects to destination server ahead of time, to avoid TCP handshake latency.
// [NOTE] Firefox will perform DNS lookup (if enabled) and TCP and TLS handshake,
// but will not start sending or receiving HTTP data.
// [1] https://www.ghacks.net/2017/07/24/disable-preloading-firefox-autocomplete-urls/
user_pref("browser.urlbar.speculativeConnect.enabled", false);

// PREF: mousedown speculative connections on bookmarks and history [FF98+]
// Whether to warm up network connections for places:menus and places:toolbar.
user_pref("browser.places.speculativeConnect.enabled", false);

// PREF: network module preload <link rel="modulepreload"> [FF115+]
// High-priority loading of current page JavaScript modules.
// Used to preload high-priority JavaScript modules for strategic performance improvements.
// Module preloading allows developers to fetch JavaScript modules and dependencies
// earlier to accelerate page loads. The browser downloads, parses, and compiles modules
// referenced by links with this attribute in parallel with other resources, rather
// than sequentially waiting to process each. Preloading reduces overall download times.
// Browsers may also automatically preload dependencies without firing extra events.
// Unlike other pre-connection tags (except rel=preload), this tag is mandatory for the browser.
// [1] https://developer.mozilla.org/en-US/docs/Web/HTML/Attributes/rel/modulepreload
//user_pref("network.modulepreload", true); // DEFAULT

// PREF: link prefetching <link rel="prefetch">
// Pre-populates the HTTP cache by prefetching same-site future navigation
// resources or subresources used on those pages.
// Enabling link prefetching allows Firefox to preload pages tagged as important.
// The browser prefetches links with the prefetch-link tag, fetching resources
// likely needed for the next navigation at low priority. When clicking a link
// or loading a new page, prefetching stops and discards hints. Prefetching
// downloads resources without executing them.
// [NOTE] Since link prefetch uses the HTTP cache, it has a number of issues
// with document prefetches, such as being potentially blocked by Cache-Control headers
// (e.g. cache partitioning).
// [1] https://developer.mozilla.org/en-US/docs/Glossary/Prefetch
// [2] http://www.mecs-press.org/ijieeb/ijieeb-v7-n5/IJIEEB-V7-N5-2.pdf
// [3] https://timkadlec.com/remembers/2020-06-17-prefetching-at-this-age/
// [4] https://3perf.com/blog/link-rels/#prefetch
// [5] https://developer.mozilla.org/docs/Web/HTTP/Link_prefetching_FAQ
user_pref("network.prefetch-next", false);

// PREF: Fetch Priority API [FF119+]
// Indicates whether the `fetchpriority` attribute for elements which support it.
// [1] https://web.dev/articles/fetch-priority
// [2] https://nitropack.io/blog/post/priority-hints
// [2] https://developer.mozilla.org/en-US/docs/Web/API/HTMLImageElement/fetchPriority
// [3] https://developer.mozilla.org/en-US/docs/Web/API/HTMLLinkElement/fetchPriority
//user_pref("network.fetchpriority.enabled", true);

// PREF: early hints [FF120+]
// [1] https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/103
// [2] https://developer.chrome.com/blog/early-hints/
// [3] https://blog.cloudflare.com/early-hints/
// [4] https://blog.cloudflare.com/early-hints-performance/
//user_pref("network.early-hints.enabled", true);

// PREF: `Link: rel=preconnect` in 103 Early Hint response [FF120+]
// Used to warm most critical cross-origin connections to provide
// performance improvements when connecting to them.
// [NOTE] When 0, this is limited by "network.http.speculative-parallel-limit".
//user_pref("network.early-hints.preconnect.enabled", true);
//user_pref("network.early-hints.preconnect.max_connections", 10); // DEFAULT

// PREF: Network Predictor (NP)
// When enabled, it trains and uses Firefox's algorithm to preload page resource
// by tracking past page resources. It uses a local file (history) of needed images,
// scripts, etc. to request them preemptively when navigating.
// [NOTE] By default, it only preconnects DNS, TCP, and SSL handshakes.
// No data sends until clicking. With "network.predictor.enable-prefetch" enabled,
// it also performs prefetches.
// [1] https://wiki.mozilla.org/Privacy/Reviews/Necko
// [2] https://www.ghacks.net/2014/05/11/seer-disable-firefox/
// [3] https://github.com/dillbyrne/random-agent-spoofer/issues/238#issuecomment-110214518
// [4] https://www.igvita.com/posa/high-performance-networking-in-google-chrome/#predictor
user_pref("network.predictor.enabled", false);

// PREF: Network Predictor fetch for resources ahead of time
// Prefetch page resources based on past user behavior.
//user_pref("network.predictor.enable-prefetch", false); // DEFAULT

// PREF: make Network Predictor active when hovering over links
// When hovering over links, Network Predictor uses past resource history to
// preemptively request what will likely be needed instead of waiting for the document.
// Predictive connections automatically open when hovering over links to speed up
// loading, starting some work in advance.
//user_pref("network.predictor.enable-hover-on-ssl", false); // DEFAULT

// PREF: assign Network Predictor confidence levels
// [NOTE] Keep in mind that Network Predictor must LEARN your browsing habits.
// Editing these lower will cause more speculative connections to occur,
// which reduces accuracy over time and has privacy implications.
//user_pref("network.predictor.preresolve-min-confidence", 60); // DEFAULT
//user_pref("network.predictor.preconnect-min-confidence", 90); // DEFAULT
//user_pref("network.predictor.prefetch-min-confidence", 100); // DEFAULT

// PREF: other Network Predictor values
// [NOTE] Keep in mmind that Network Predictor must LEARN your browsing habits.
//user_pref("network.predictor.prefetch-force-valid-for", 10); // DEFAULT; how long prefetched resources are considered valid and usable (in seconds) for the prediction modeling
//user_pref("network.predictor.prefetch-rolling-load-count", 10); // DEFAULT; the maximum number of resources that Firefox will prefetch in memory at one time based on prediction modeling
//user_pref("network.predictor.max-resources-per-entry", 250); // default=100
//user_pref("network.predictor.max-uri-length", 1000); // default=500

/****************************************************************************
 * SECTION: EXPERIMENTAL                                                    *
****************************************************************************/

// PREF: CSS Masonry Layout [NIGHTLY]
// [1] https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Grid_Layout/Masonry_Layout
// [2] https://www.smashingmagazine.com/native-css-masonry-layout-css-grid/
//user_pref("layout.css.grid-template-masonry-value.enabled", true);

/****************************************************************************
 * SECTION: TAB UNLOAD                                                      *
****************************************************************************/

// PREF: unload tabs on low memory
// [ABOUT] about:unloads
// Firefox will detect if your computer’s memory is running low (less than 200MB)
// and suspend tabs that you have not used in awhile.
// [1] https://support.mozilla.org/en-US/kb/unload-inactive-tabs-save-system-memory-firefox
// [2] https://hacks.mozilla.org/2021/10/tab-unloading-in-firefox-93/
//user_pref("browser.tabs.unloadOnLowMemory", true); // DEFAULT

// PREF: determine when tabs unload [WINDOWS] [LINUX]
// Notify TabUnloader or send the memory pressure if the memory resource
// notification is signaled AND the available commit space is lower than
// this value (in MiB).
// Set this to some value, e.g. 4/5 of total memory available on your system:
// 4GB=3276, 8GB=6553, 16GB=13107, 32GB=25698, 64GB=52429
// [1] https://dev.to/msugakov/taking-firefox-memory-usage-under-control-on-linux-4b02
//user_pref("browser.low_commit_space_threshold_mb", 3276); // default=200; WINDOWS LINUX

// PREF: determine when tabs unload [LINUX]
// On Linux, Firefox checks available memory in comparison to total memory,
// and use this percent value (out of 100) to determine if Firefox is in a
// low memory scenario.
// [1] https://dev.to/msugakov/taking-firefox-memory-usage-under-control-on-linux-4b02
//user_pref("browser.low_commit_space_threshold_percent", 20); // default=5; LINUX

// PREF: determine how long (in ms) tabs are inactive before they unload
// 60000=1min; 300000=5min; 600000=10min (default)
//user_pref("browser.tabs.min_inactive_duration_before_unload", 300000); // 5min; default=600000

/****************************************************************************
 * SECTION: PROCESS COUNT                                                  *
****************************************************************************/

// PREF: process count
// [ABOUT] View in about:processes.
// With Firefox Quantum (2017), CPU cores = processCount. However, since the
// introduction of Fission [2], the number of website processes is controlled
// by processCount.webIsolated. Disabling fission.autostart or changing
// fission.webContentIsolationStrategy reverts control back to processCount.
// [1] https://www.reddit.com/r/firefox/comments/r69j52/firefox_content_process_limit_is_gone/
// [2] https://firefox-source-docs.mozilla.org/dom/ipc/process_model.html#web-content-processes 
//user_pref("dom.ipc.processCount", 8); // DEFAULT; Shared Web Content
//user_pref("dom.ipc.processCount.webIsolated", 1); // default=4; Isolated Web Content
//user_pref("dom.ipc.keepProcessesAlive.web", 4); // default=1 [HIDDEN OR REMOVED]

// PREF: use one process for process preallocation cache
//user_pref("dom.ipc.processPrelaunch.fission.number", 1); // default=3; Process Preallocation Cache

// PREF: configure process isolation
// [1] https://hg.mozilla.org/mozilla-central/file/tip/dom/ipc/ProcessIsolation.cpp#l53
// [2] https://www.reddit.com/r/firefox/comments/r69j52/firefox_content_process_limit_is_gone/

// OPTION 1: isolate all websites
// Web content is always isolated into its own `webIsolated` content process
// based on site-origin, and will only load in a shared `web` content process
// if site-origin could not be determined.
//user_pref("fission.webContentIsolationStrategy", 1); // DEFAULT
//user_pref("browser.preferences.defaultPerformanceSettings.enabled", true); // DEFAULT
    //user_pref("dom.ipc.processCount.webIsolated", 1); // one process per site origin

// OPTION 2: isolate only "high value" websites
// Only isolates web content loaded by sites which are considered "high
// value". A site is considered high value if it has been granted a
// `highValue*` permission by the permission manager, which is done in
// response to certain actions.
//user_pref("fission.webContentIsolationStrategy", 2);
//user_pref("browser.preferences.defaultPerformanceSettings.enabled", false);
    //user_pref("dom.ipc.processCount.webIsolated", 1); // one process per site origin (high value)
    //user_pref("dom.ipc.processCount", 8); // determine by number of CPU cores/processors

// OPTION 3: do not isolate websites
// All web content is loaded into a shared `web` content process. This is
// similar to the non-Fission behavior; however, remote subframes may still
// be used for sites with special isolation behavior, such as extension or
// mozillaweb content processes.
//user_pref("fission.webContentIsolationStrategy", 0);
//user_pref("browser.preferences.defaultPerformanceSettings.enabled", false);
    //user_pref("dom.ipc.processCount", 8); // determine by number of CPU cores/processors

/****************************************************************************
 * Securefox                                                                *
 * "Natura non contristatur"                                                *     
 * priority: provide sensible security and privacy                          *
 * version: 144                                                             *
 * url: https://github.com/yokoffing/Betterfox                              *
 * credit: Most prefs are reproduced and adapted from the arkenfox project  *
 * credit urL: https://github.com/arkenfox/user.js                          *
****************************************************************************/

/****************************************************************************
 * SECTION: TRACKING PROTECTION                                             *
****************************************************************************/

// PREF: Enhanced Tracking Protection (ETP)
// Tracking Content blocking will strip cookies and block all resource requests to domains listed in Disconnect.me.
// Firefox deletes all stored site data (incl. cookies, browser storage) if the site is a known tracker and hasn’t
// been interacted with in the last 30 days.
// [ALLOWLIST] https://disconnect.me/trackerprotection/unblocked
// [NOTE] FF86: "Strict" tracking protection enables dFPI.
// [1] https://support.mozilla.org/en-US/kb/enhanced-tracking-protection-firefox-desktop
// [2] https://www.reddit.com/r/firefox/comments/l7xetb/network_priority_for_firefoxs_enhanced_tracking/gle2mqn/?web2x&context=3
user_pref("browser.contentblocking.category", "strict"); // [HIDDEN]
// [1] https://bugzilla.mozilla.org/show_bug.cgi?id=1970647
user_pref("privacy.trackingprotection.allow_list.baseline.enabled", true); // [FF142+]
//user_pref("privacy.trackingprotection.allow_list.convenience.enabled", true); // [FF142+]
//user_pref("privacy.trackingprotection.enabled", true); // enabled with "Strict"
//user_pref("privacy.trackingprotection.pbmode.enabled", true); // DEFAULT
//user_pref("browser.contentblocking.customBlockList.preferences.ui.enabled", false); // DEFAULT
//user_pref("privacy.trackingprotection.socialtracking.enabled", true); // enabled with "Strict"
    //user_pref("privacy.socialtracking.block_cookies.enabled", true); // DEFAULT
//user_pref("privacy.trackingprotection.cryptomining.enabled", true); // DEFAULT
//user_pref("privacy.trackingprotection.fingerprinting.enabled", true); // DEFAULT
//user_pref("privacy.trackingprotection.emailtracking.enabled", true); // enabled with "Strict"
//user_pref("network.http.referer.disallowCrossSiteRelaxingDefault", true); // DEFAULT
    //user_pref("network.http.referer.disallowCrossSiteRelaxingDefault.pbmode", true); // DEFAULT
    //user_pref("network.http.referer.disallowCrossSiteRelaxingDefault.pbmode.top_navigation", true); // DEFAULT
    //user_pref("network.http.referer.disallowCrossSiteRelaxingDefault.top_navigation", true); // enabled with "Strict"
//user_pref("privacy.annotate_channels.strict_list.enabled", true); // enabled with "Strict"
    //user_pref("privacy.annotate_channels.strict_list.pbmode.enabled", true); // DEFAULT
//user_pref("privacy.fingerprintingProtection", true); // [FF114+] [ETP FF119+] enabled with "Strict"
    //user_pref("privacy.fingerprintingProtection.pbmode", true); // DEFAULT
//user_pref("privacy.bounceTrackingProtection.mode", 1); // [FF131+] [ETP FF133+]
// [1] https://searchfox.org/mozilla-central/source/toolkit/components/antitracking/bouncetracking


// PREF: disable Firefox Suggest
// [1] https://github.com/arkenfox/user.js/issues/1257
user_pref("browser.urlbar.quicksuggest.enabled", false); // controls whether the UI is shown
    //user_pref("browser.urlbar.suggest.quicksuggest.sponsored", false); // [FF92+] 
    //user_pref("browser.urlbar.suggest.quicksuggest.nonsponsored", false); // [FF95+]
// hide Firefox Suggest label in URL dropdown box
user_pref("browser.urlbar.groupLabels.enabled", false);

// PREF: disable search and form history
// Be aware that autocomplete form data can be read by third parties [1][2].
// Form data can easily be stolen by third parties.
// [SETTING] Privacy & Security>History>Custom Settings>Remember search and form history
// [1] https://blog.mindedsecurity.com/2011/10/autocompleteagain.html
// [2] https://bugzilla.mozilla.org/381681
user_pref("browser.formfill.enable", false);


// PREF: disable formless login capture for Password Manager [FF51+]
// [1] https://bugzilla.mozilla.org/show_bug.cgi?id=1166947
user_pref("signon.formlessCapture.enabled", false);

// PREF: disable capturing credentials in private browsing
user_pref("signon.privateBrowsingCapture.enabled", false);

// * OPTION: NATURAL SMOOTH SCROLLING V3 [MODIFIED]*****************************************************************************************/
// credit: https://github.com/AveYo/fox/blob/cf56d1194f4e5958169f9cf335cd175daa48d349/Natural%20Smooth%20Scrolling%20for%20user.js
// recommended for 120hz+ displays
// largely matches Chrome flags: Windows Scrolling Personality and Smooth Scrolling
user_pref("apz.overscroll.enabled", true); // DEFAULT NON-LINUX
user_pref("general.smoothScroll", true); // DEFAULT
user_pref("general.smoothScroll.msdPhysics.continuousMotionMaxDeltaMS", 12);
user_pref("general.smoothScroll.msdPhysics.enabled", true);
user_pref("general.smoothScroll.msdPhysics.motionBeginSpringConstant", 600);
user_pref("general.smoothScroll.msdPhysics.regularSpringConstant", 650);
user_pref("general.smoothScroll.msdPhysics.slowdownMinDeltaMS", 25);
user_pref("general.smoothScroll.msdPhysics.slowdownMinDeltaRatio", "2");
user_pref("general.smoothScroll.msdPhysics.slowdownSpringConstant", 250);
user_pref("general.smoothScroll.currentVelocityWeighting", "1");
user_pref("general.smoothScroll.stopDecelerationWeighting", "1");
user_pref("mousewheel.default.delta_multiplier_y", 260); // 250-400 levels
