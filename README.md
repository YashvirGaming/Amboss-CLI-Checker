<h1>Amboss CLI Checker</h1>

<p>
  <img src="https://img.shields.io/badge/Python-3.10+-blue" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green" alt="License">
  <img src="https://img.shields.io/badge/Platform-Windows-lightgrey" alt="Platform">
</p>

<p>A high-performance CLI checker for <strong>Amboss</strong>, built with <code>httpx</code>, multi-threading, and advanced proxy support (HTTP/HTTPS with <code>ip:port:user:pass</code> fallback to <code>ip:port</code>). Features live CPM counter, colorful CLI output, and capture printing/writing for <em>Hits</em> &amp; <em>Custom</em> accounts.</p>

<h2>✨ Features</h2>
<ul>
  <li>Premium CLI design with ASCII Shadow font art and two-line colored subtitle.</li>
  <li>Full <strong>httpx</strong> networking with automatic Content-Length handling.</li>
  <li>Proxy parsing for both <code>ip:port:user:pass</code> and <code>ip:port</code> formats.</li>
  <li>No auto-strip on combo/proxy loading (preserves original formatting).</li>
  <li>Multi-threaded with live CPM tracking.</li>
  <li>Captures: <code>hasAccess</code>, <code>hasFreeAccess</code>, <code>ExpiryDate</code>.</li>
  <li>Writes results only for Hits (<code>Hits.txt</code>) and Custom (<code>Custom.txt</code>).</li>
  <li>No file writing for Fails.</li>
</ul>

<h2>📦 Requirements</h2>
<pre><code>httpx
colorama
</code></pre>

<h2>🚀 Usage</h2>
<ol>
  <li>Install Python 3.10+ and required packages:<br>
    <code>pip install -r requirements.txt</code>
  </li>
  <li>Run the checker:<br>
    <code>python Amboss_Checker.py</code>
  </li>
  <li>Drop your combos file and proxies file when prompted.</li>
</ol>

<h2>🛠 Build to EXE with Nuitka</h2>
<p>Use the included <code>Builder.bat</code>:</p>
<pre><code>@echo off
title Nuitka Builder - Amboss Checker
set "SCRIPT=Amboss_Checker.py"

python -m nuitka ^
--standalone ^
--onefile ^
--jobs=12 ^
--include-module=httpx ^
--include-module=colorama ^
--output-filename=Amboss_Checker.exe ^
%SCRIPT%

pause
</code></pre>

<h2>💬 Credits</h2>
<p>
Made with ❤️ by <strong>Yashvir Gaming</strong><br>
Telegram: <a href="https://t.me/therealyashvirgaming" target="_blank">https://t.me/therealyashvirgaming</a>
</p>
