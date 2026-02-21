#!/usr/bin/env python3
"""Generate enhanced Complyr pitch deck HTML."""

HEAD = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Complyr - Hackathon Pitch</title>
<script src="https://cdn.tailwindcss.com"></script>
<script src="https://unpkg.com/lucide@latest"></script>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Poppins:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<script>
tailwind.config={theme:{extend:{fontFamily:{sans:['Inter','sans-serif'],display:['Poppins','sans-serif']},colors:{navy:{900:'#0B1C2D',800:'#112233',700:'#1a3349'},electric:{500:'#3B82F6',600:'#2563EB',400:'#60A5FA'}},animation:{'fade-in':'fadeIn 0.8s ease-out','slide-up':'slideUp 0.6s ease-out','pulse-glow':'pulseGlow 2s ease-in-out infinite','float':'float 6s ease-in-out infinite','gradient-x':'gradientX 3s linear infinite','drift':'drift 20s linear infinite','counter':'counter 2s ease-out forwards'},keyframes:{fadeIn:{'0%':{opacity:'0'},'100%':{opacity:'1'}},slideUp:{'0%':{opacity:'0',transform:'translateY(30px)'},'100%':{opacity:'1',transform:'translateY(0)'}},pulseGlow:{'0%, 100%':{boxShadow:'0 0 20px rgba(37,99,235,0.3)'},'50%':{boxShadow:'0 0 40px rgba(37,99,235,0.6)'}},float:{'0%, 100%':{transform:'translateY(0)'},'50%':{transform:'translateY(-20px)'}},gradientX:{'0%, 100%':{'background-position':'0% 50%'},'50%':{'background-position':'100% 50%'}},drift:{'0%':{transform:'translate(0,0) rotate(0deg)'},'25%':{transform:'translate(50px,-30px) rotate(5deg)'},'50%':{transform:'translate(-20px,-60px) rotate(-3deg)'},'75%':{transform:'translate(-50px,20px) rotate(4deg)'},'100%':{transform:'translate(0,0) rotate(0deg)'}}}}}}
</script>
<style>
body{overflow:hidden;background:#0B1C2D}
.slide{position:absolute;width:100vw;height:100vh;display:none;opacity:0;transition:opacity 0.5s ease-in-out}
.slide.active{display:flex;opacity:1}
.glass-card{background:linear-gradient(145deg,rgba(30,41,59,0.8),rgba(15,23,42,0.9));backdrop-filter:blur(20px);border:1px solid rgba(255,255,255,0.1);box-shadow:0 25px 50px -12px rgba(0,0,0,0.5)}
.text-gradient{background:linear-gradient(90deg,#60A5FA,#2563EB,#93C5FD);background-size:200% auto;-webkit-background-clip:text;-webkit-text-fill-color:transparent;animation:gradientX 3s linear infinite}
.grid-bg{background-image:linear-gradient(rgba(37,99,235,0.1) 1px,transparent 1px),linear-gradient(90deg,rgba(37,99,235,0.1) 1px,transparent 1px);background-size:50px 50px}
.orb{position:absolute;border-radius:50%;filter:blur(60px);opacity:0.4;animation:float 8s ease-in-out infinite}
.progress-bar{position:fixed;bottom:0;left:0;height:4px;background:linear-gradient(90deg,#2563EB,#60A5FA);transition:width 0.3s ease;z-index:50}
.nav-dots{position:fixed;right:30px;top:50%;transform:translateY(-50%);display:flex;flex-direction:column;gap:10px;z-index:50}
.nav-dot{width:10px;height:10px;border-radius:50%;background:rgba(255,255,255,0.2);cursor:pointer;transition:all 0.3s ease;border:2px solid transparent}
.nav-dot.active{background:#2563EB;border-color:#60A5FA;transform:scale(1.3);box-shadow:0 0 15px rgba(37,99,235,0.6)}
.tech-card:hover{transform:translateY(-5px);box-shadow:0 20px 40px rgba(37,99,235,0.3);border-color:rgba(37,99,235,0.5)}
.feature-icon{transition:all 0.3s ease}
.feature-card:hover .feature-icon{transform:scale(1.1) rotate(5deg);filter:drop-shadow(0 0 10px rgba(37,99,235,0.6))}
.floating-icon{position:absolute;opacity:0.06;animation:drift 20s linear infinite;pointer-events:none}
.tricolor-bar{height:3px;background:linear-gradient(90deg,#FF9933 33%,#FFFFFF 33%,#FFFFFF 66%,#138808 66%);opacity:0.4;border-radius:2px}
.glow-stat{box-shadow:0 0 30px rgba(37,99,235,0.2);border:1px solid rgba(37,99,235,0.3)}
.sub-explain{color:#94a3b8;font-size:0.875rem;font-style:italic;margin-top:0.25rem}
.flow-step{opacity:0;transform:translateY(20px);transition:all 0.6s ease}
.flow-step.visible{opacity:1;transform:translateY(0)}
.flow-arrow{opacity:0;transition:opacity 0.4s ease}
.flow-arrow.visible{opacity:1}
.disconnect-pulse{animation:pulseGlow 1.5s ease-in-out infinite}
</style>
</head>
<body class="text-white antialiased">
'''

TOTAL = 11

def nav_dots():
    dots = ''.join(f'<div class="nav-dot {"active" if i==0 else ""}" onclick="goToSlide({i})"></div>' for i in range(TOTAL))
    return f'''<div class="progress-bar" id="progressBar" style="width:{100/TOTAL:.1f}%"></div>
<div class="nav-dots" id="navDots">{dots}</div>
<div class="fixed bottom-6 left-6 text-xs text-slate-500 font-mono z-50">Use ← → arrow keys to navigate</div>
<div class="tricolor-bar fixed top-0 left-0 w-full z-50"></div>'''

def floating_icons():
    icons = [
        ('shield','top:10%;left:5%','0s'),('file-text','top:60%;left:85%','5s'),
        ('database','top:30%;right:10%','10s'),('alert-triangle','bottom:20%;left:15%','15s'),
        ('check-circle','top:70%;right:25%','8s')
    ]
    return ''.join(f'<div class="floating-icon" style="{pos};animation-delay:{d}"><i data-lucide="{ic}" class="w-16 h-16"></i></div>' for ic,pos,d in icons)

SLIDE1 = '''<div class="slide active" id="slide0">
<div class="absolute inset-0 grid-bg opacity-30"></div>
<div class="orb w-96 h-96 bg-blue-600 top-0 left-0"></div>
<div class="orb w-64 h-64 bg-indigo-600 bottom-0 right-0" style="animation-delay:-4s"></div>
''' + floating_icons() + '''
<div class="relative z-10 flex flex-col items-center justify-center h-full px-8">
<div class="animate-fade-in text-center">
<div class="inline-flex items-center gap-3 px-5 py-2 rounded-full glass-card border border-blue-500/30 mb-8">
<span class="flex h-2 w-2 rounded-full bg-blue-400 animate-pulse"></span>
<span class="text-blue-200 text-sm font-medium tracking-wide">HACKFEST 2.0</span>
</div>
<div class="flex items-center justify-center gap-4 mb-6">
<div class="w-16 h-16 bg-gradient-to-br from-blue-500 to-blue-700 rounded-2xl flex items-center justify-center shadow-2xl shadow-blue-500/30 animate-pulse-glow">
<i data-lucide="shield-check" class="w-9 h-9 text-white"></i>
</div>
<h1 class="font-display font-black text-7xl md:text-8xl tracking-tight"><span class="text-gradient">Complyr</span></h1>
</div>
<p class="text-2xl md:text-3xl text-slate-300 font-light mb-4 max-w-3xl mx-auto leading-relaxed">AI-Powered <span class="text-blue-400 font-semibold">Continuous</span> Policy Enforcement</p>
<p class="sub-explain text-lg max-w-2xl mx-auto mb-8">Transform static compliance documents into real-time monitoring systems — automatically.</p>
<div class="flex items-center justify-center gap-8 text-sm text-slate-400 mb-6">
<div class="flex items-center gap-2"><i data-lucide="brain" class="w-4 h-4 text-blue-500"></i><span>LLM-Powered</span></div>
<div class="flex items-center gap-2"><i data-lucide="activity" class="w-4 h-4 text-blue-500"></i><span>Real-Time</span></div>
<div class="flex items-center gap-2"><i data-lucide="shield" class="w-4 h-4 text-blue-500"></i><span>Enterprise-Grade</span></div>
</div>
<div class="text-slate-500 text-sm">Designed for <span class="text-blue-400">Indian</span> and global enterprises</div>
</div></div></div>'''

SLIDE2 = '''<div class="slide" id="slide1">
<div class="absolute inset-0 bg-gradient-to-br from-navy-900 via-navy-800 to-navy-900"></div>
<div class="orb w-80 h-80 bg-red-600/30 top-10 right-10"></div>
<div class="relative z-10 flex flex-col justify-center h-full px-16 md:px-24">
<div class="max-w-6xl mx-auto w-full">
<div class="flex items-center gap-3 mb-12">
<span class="text-red-500 font-mono text-sm">01</span>
<div class="h-px flex-1 bg-gradient-to-r from-red-500/50 to-transparent"></div>
<span class="text-red-400 text-sm font-medium uppercase tracking-wider">The Problem</span>
</div>
<div class="grid md:grid-cols-2 gap-16 items-center">
<div class="animate-slide-up">
<h2 class="font-display font-bold text-5xl md:text-6xl mb-4 leading-tight">Compliance is<br/><span class="text-red-400">broken.</span></h2>
<p class="sub-explain mb-8">Companies spend thousands of hours manually checking if their data follows regulatory policies.</p>
<div class="space-y-6">
<div class="flex items-start gap-4">
<div class="w-12 h-12 rounded-xl bg-red-500/10 flex items-center justify-center flex-shrink-0 border border-red-500/20"><i data-lucide="file-text" class="w-6 h-6 text-red-400"></i></div>
<div><h3 class="text-xl font-semibold text-white mb-1">Manual Policy Review</h3><p class="text-slate-400">40+ hours per policy document. 200+ page PDFs read line by line.</p></div>
</div>
<div class="flex items-start gap-4">
<div class="w-12 h-12 rounded-xl bg-red-500/10 flex items-center justify-center flex-shrink-0 border border-red-500/20"><i data-lucide="clock" class="w-6 h-6 text-red-400"></i></div>
<div><h3 class="text-xl font-semibold text-white mb-1">Quarterly Audits</h3><p class="text-slate-400">Violations discovered months too late. Damage already done.</p></div>
</div>
<div class="flex items-start gap-4">
<div class="w-12 h-12 rounded-xl bg-red-500/10 flex items-center justify-center flex-shrink-0 border border-red-500/20"><i data-lucide="indian-rupee" class="w-6 h-6 text-red-400"></i></div>
<div><h3 class="text-xl font-semibold text-white mb-1">₹2Cr+ Average Penalty</h3><p class="text-slate-400">Per missed compliance clause. One oversight can shut down operations.</p></div>
</div>
</div></div>
<div class="glass-card p-8 rounded-2xl glow-stat animate-fade-in" style="animation-delay:0.3s">
<div class="text-center mb-8">
<div class="text-6xl font-black text-red-400 mb-2">78%</div>
<div class="text-slate-300">of enterprises still use spreadsheets for compliance</div>
</div>
<div class="space-y-4">
<div class="flex justify-between items-center text-sm"><span class="text-slate-400">Manual Hours</span><span class="text-red-400 font-mono">2,000+/year</span></div>
<div class="h-2 bg-slate-800 rounded-full overflow-hidden"><div class="h-full bg-red-500 w-[85%]"></div></div>
<div class="flex justify-between items-center text-sm"><span class="text-slate-400">Detection Delay</span><span class="text-red-400 font-mono">90 days avg</span></div>
<div class="h-2 bg-slate-800 rounded-full overflow-hidden"><div class="h-full bg-red-500 w-[70%]"></div></div>
<div class="flex justify-between items-center text-sm"><span class="text-slate-400">Error Rate</span><span class="text-red-400 font-mono">15-20%</span></div>
<div class="h-2 bg-slate-800 rounded-full overflow-hidden"><div class="h-full bg-red-500 w-[20%]"></div></div>
</div></div>
</div></div></div></div>'''

SLIDE3_GAP = '''<div class="slide" id="slide2">
<div class="absolute inset-0 bg-gradient-to-br from-navy-900 via-red-900/10 to-navy-900"></div>
<div class="orb w-72 h-72 bg-red-600/20 top-10 left-10"></div>
<div class="relative z-10 flex flex-col justify-center h-full px-16 md:px-24">
<div class="max-w-5xl mx-auto w-full text-center">
<div class="flex items-center justify-center gap-3 mb-8">
<span class="text-amber-500 font-mono text-sm">02</span>
<span class="text-amber-400 text-sm font-medium uppercase tracking-wider">⚠ The Compliance Gap</span>
</div>
<h2 class="font-display font-bold text-4xl md:text-5xl mb-6">The <span class="text-red-400">Disconnect</span></h2>
<p class="sub-explain text-lg mb-12">Policies live in documents. Company data lives in databases. Nothing connects them automatically.</p>
<div class="flex items-center justify-center gap-6 md:gap-12 flex-wrap">
<div class="glass-card p-6 rounded-2xl text-center w-48">
<div class="w-16 h-16 mx-auto mb-3 rounded-2xl bg-amber-500/10 flex items-center justify-center border border-amber-500/20"><i data-lucide="file-stack" class="w-8 h-8 text-amber-400"></i></div>
<div class="text-white font-semibold mb-1">Policy PDFs</div>
<div class="text-slate-400 text-xs">200+ pages of dense regulatory text</div>
</div>
<div class="flex flex-col items-center gap-2 disconnect-pulse">
<div class="w-16 h-16 rounded-full bg-red-500/20 flex items-center justify-center border-2 border-red-500/40"><i data-lucide="unplug" class="w-8 h-8 text-red-400"></i></div>
<span class="text-red-400 text-xs font-mono">GAP</span>
</div>
<div class="glass-card p-6 rounded-2xl text-center w-48">
<div class="w-16 h-16 mx-auto mb-3 rounded-2xl bg-blue-500/10 flex items-center justify-center border border-blue-500/20"><i data-lucide="database" class="w-8 h-8 text-blue-400"></i></div>
<div class="text-white font-semibold mb-1">Company Data</div>
<div class="text-slate-400 text-xs">Millions of records changing every second</div>
</div>
</div>
<div class="mt-12 space-y-3 text-left max-w-2xl mx-auto">
<div class="flex items-center gap-3 glass-card px-5 py-3 rounded-xl"><i data-lucide="file-text" class="w-5 h-5 text-amber-400 flex-shrink-0"></i><span class="text-slate-300 text-sm">Policies are written in complex legal documents</span></div>
<div class="flex items-center gap-3 glass-card px-5 py-3 rounded-xl"><i data-lucide="refresh-cw" class="w-5 h-5 text-blue-400 flex-shrink-0"></i><span class="text-slate-300 text-sm">Company data changes every second</span></div>
<div class="flex items-center gap-3 glass-card px-5 py-3 rounded-xl"><i data-lucide="alert-triangle" class="w-5 h-5 text-red-400 flex-shrink-0"></i><span class="text-slate-300 text-sm">Manual compliance checks are slow, expensive, and error-prone</span></div>
</div>
<div class="mt-6 text-slate-500 text-xs">Example: <span class="text-amber-400 font-mono">"Transactions above ₹5,00,000 require dual approval"</span> — who checks this in real time?</div>
</div></div></div>'''

SLIDE4_COMPARE = '''<div class="slide" id="slide3">
<div class="absolute inset-0 bg-gradient-to-br from-navy-900 to-navy-800"></div>
<div class="orb w-64 h-64 bg-blue-600/20 bottom-10 right-10"></div>
<div class="relative z-10 flex flex-col justify-center h-full px-16 md:px-24">
<div class="max-w-5xl mx-auto w-full">
<div class="flex items-center gap-3 mb-8">
<span class="text-blue-500 font-mono text-sm">03</span>
<div class="h-px flex-1 bg-gradient-to-r from-blue-500/50 to-transparent"></div>
<span class="text-blue-400 text-sm font-medium uppercase tracking-wider">Why Change?</span>
</div>
<h2 class="font-display font-bold text-4xl md:text-5xl mb-12 text-center">Traditional vs <span class="text-gradient">Complyr</span></h2>
<div class="grid md:grid-cols-2 gap-8">
<div class="glass-card p-8 rounded-2xl border border-red-500/20">
<h3 class="text-xl font-bold text-red-400 mb-6 flex items-center gap-2"><i data-lucide="x-circle" class="w-6 h-6"></i> Traditional Compliance</h3>
<div class="space-y-4">
<div class="flex items-center gap-3"><span class="text-red-400">✗</span><span class="text-slate-300">Manual review of policy documents</span></div>
<div class="flex items-center gap-3"><span class="text-red-400">✗</span><span class="text-slate-300">Delayed detection — weeks to months</span></div>
<div class="flex items-center gap-3"><span class="text-red-400">✗</span><span class="text-slate-300">High audit risk &amp; human error</span></div>
<div class="flex items-center gap-3"><span class="text-red-400">✗</span><span class="text-slate-300">No real-time visibility</span></div>
<div class="flex items-center gap-3"><span class="text-red-400">✗</span><span class="text-slate-300">Expensive consulting fees</span></div>
</div>
<div class="mt-6 text-red-400/60 text-sm font-mono">Cost: ₹50L+ per year</div>
</div>
<div class="glass-card p-8 rounded-2xl border border-green-500/20 glow-stat">
<h3 class="text-xl font-bold text-green-400 mb-6 flex items-center gap-2"><i data-lucide="check-circle" class="w-6 h-6"></i> With Complyr</h3>
<div class="space-y-4">
<div class="flex items-center gap-3"><span class="text-green-400">✓</span><span class="text-slate-300">Automated rule extraction from PDFs</span></div>
<div class="flex items-center gap-3"><span class="text-green-400">✓</span><span class="text-slate-300">Continuous real-time monitoring</span></div>
<div class="flex items-center gap-3"><span class="text-green-400">✓</span><span class="text-slate-300">Explainable AI-powered alerts</span></div>
<div class="flex items-center gap-3"><span class="text-green-400">✓</span><span class="text-slate-300">Instant violation dashboard</span></div>
<div class="flex items-center gap-3"><span class="text-green-400">✓</span><span class="text-slate-300">Audit-ready compliance reports</span></div>
</div>
<div class="mt-6 text-green-400/60 text-sm font-mono">Save up to 95% time &amp; cost</div>
</div>
</div></div></div></div>'''

SLIDE5_SOLUTION = '''<div class="slide" id="slide4">
<div class="absolute inset-0 bg-gradient-to-br from-navy-900 via-blue-900/20 to-navy-900"></div>
<div class="orb w-96 h-96 bg-blue-600/20 bottom-0 left-0"></div>
<div class="relative z-10 flex flex-col justify-center h-full px-16 md:px-24">
<div class="max-w-6xl mx-auto w-full">
<div class="flex items-center gap-3 mb-8">
<span class="text-blue-500 font-mono text-sm">04</span>
<div class="h-px flex-1 bg-gradient-to-r from-blue-500/50 to-transparent"></div>
<span class="text-blue-400 text-sm font-medium uppercase tracking-wider">The Solution</span>
</div>
<h2 class="font-display font-bold text-4xl md:text-5xl mb-4 text-center">From <span class="text-slate-500">PDFs</span> to <span class="text-gradient">Protection</span></h2>
<p class="sub-explain text-center mb-10">Our AI reads your policies, understands the rules, and continuously checks your data for violations.</p>
<div class="grid md:grid-cols-4 gap-6">
<div class="feature-card glass-card p-6 rounded-2xl text-center group animate-slide-up relative">
<div class="feature-icon w-16 h-16 mx-auto mb-4 rounded-2xl bg-blue-500/10 flex items-center justify-center border border-blue-500/20"><i data-lucide="upload" class="w-8 h-8 text-blue-400"></i></div>
<div class="text-blue-400 font-mono text-sm mb-2">01</div>
<h3 class="text-xl font-bold text-white mb-1">Upload</h3>
<p class="text-slate-400 text-sm">Policy PDFs</p>
<p class="sub-explain text-xs mt-2">Simply drag and drop your compliance documents</p>
<div class="hidden md:block absolute top-1/2 -right-3 w-6 h-[2px] bg-gradient-to-r from-blue-500/50 to-transparent"></div>
</div>
<div class="feature-card glass-card p-6 rounded-2xl text-center group animate-slide-up relative" style="animation-delay:0.15s">
<div class="feature-icon w-16 h-16 mx-auto mb-4 rounded-2xl bg-indigo-500/10 flex items-center justify-center border border-indigo-500/20"><i data-lucide="brain" class="w-8 h-8 text-indigo-400"></i></div>
<div class="text-indigo-400 font-mono text-sm mb-2">02</div>
<h3 class="text-xl font-bold text-white mb-1">Extract</h3>
<p class="text-slate-400 text-sm">AI Rules</p>
<p class="sub-explain text-xs mt-2">AI converts legal text into machine-readable rules</p>
<div class="hidden md:block absolute top-1/2 -right-3 w-6 h-[2px] bg-gradient-to-r from-blue-500/50 to-transparent"></div>
</div>
<div class="feature-card glass-card p-6 rounded-2xl text-center group animate-slide-up relative" style="animation-delay:0.3s">
<div class="feature-icon w-16 h-16 mx-auto mb-4 rounded-2xl bg-purple-500/10 flex items-center justify-center border border-purple-500/20"><i data-lucide="database" class="w-8 h-8 text-purple-400"></i></div>
<div class="text-purple-400 font-mono text-sm mb-2">03</div>
<h3 class="text-xl font-bold text-white mb-1">Connect</h3>
<p class="text-slate-400 text-sm">Database</p>
<p class="sub-explain text-xs mt-2">Securely link to your company's existing databases</p>
<div class="hidden md:block absolute top-1/2 -right-3 w-6 h-[2px] bg-gradient-to-r from-blue-500/50 to-transparent"></div>
</div>
<div class="feature-card glass-card p-6 rounded-2xl text-center group animate-slide-up relative" style="animation-delay:0.45s">
<div class="feature-icon w-16 h-16 mx-auto mb-4 rounded-2xl bg-green-500/10 flex items-center justify-center border border-green-500/20"><i data-lucide="shield-check" class="w-8 h-8 text-green-400"></i></div>
<div class="text-green-400 font-mono text-sm mb-2">04</div>
<h3 class="text-xl font-bold text-white mb-1">Monitor</h3>
<p class="text-slate-400 text-sm">Real-time</p>
<p class="sub-explain text-xs mt-2">Continuous scanning detects violations instantly</p>
</div>
</div>
<div class="mt-10 glass-card p-5 rounded-xl max-w-3xl mx-auto">
<div class="flex items-center gap-4">
<div class="w-12 h-12 rounded-full bg-green-500/20 flex items-center justify-center"><i data-lucide="check-circle" class="w-6 h-6 text-green-400"></i></div>
<div><div class="text-white font-semibold">Result: Continuous Compliance</div>
<div class="text-slate-400 text-sm">AI detects violations in <span class="text-blue-400 font-mono">milliseconds</span>, not months</div></div>
</div></div></div></div></div>'''

SLIDE6_FLOW = '''<div class="slide" id="slide5">
<div class="absolute inset-0 bg-navy-900"></div>
<div class="orb w-64 h-64 bg-blue-600/15 top-20 left-20"></div>
<div class="relative z-10 flex flex-col justify-center h-full px-16 md:px-24">
<div class="max-w-5xl mx-auto w-full text-center">
<div class="flex items-center justify-center gap-3 mb-8">
<span class="text-blue-500 font-mono text-sm">05</span>
<span class="text-blue-400 text-sm font-medium uppercase tracking-wider">How It Works</span>
</div>
<h2 class="font-display font-bold text-4xl md:text-5xl mb-4">The <span class="text-gradient">Complyr</span> Pipeline</h2>
<p class="sub-explain text-lg mb-12">Complyr connects unstructured policies with structured company data — automatically.</p>
<div class="flex items-center justify-center gap-3 md:gap-4 flex-wrap" id="flowDiagram">
<div class="flow-step glass-card p-4 rounded-xl text-center w-32" data-step="0">
<i data-lucide="file-text" class="w-8 h-8 text-amber-400 mx-auto mb-2"></i>
<div class="text-white text-sm font-semibold">PDF</div>
<div class="text-slate-500 text-xs">Policy docs</div></div>
<div class="flow-arrow text-blue-500 text-2xl" data-step="1">→</div>
<div class="flow-step glass-card p-4 rounded-xl text-center w-32" data-step="2">
<i data-lucide="bot" class="w-8 h-8 text-blue-400 mx-auto mb-2"></i>
<div class="text-white text-sm font-semibold">AI Agent</div>
<div class="text-slate-500 text-xs">Rule extraction</div></div>
<div class="flow-arrow text-blue-500 text-2xl" data-step="3">→</div>
<div class="flow-step glass-card p-4 rounded-xl text-center w-32" data-step="4">
<i data-lucide="database" class="w-8 h-8 text-purple-400 mx-auto mb-2"></i>
<div class="text-white text-sm font-semibold">Database</div>
<div class="text-slate-500 text-xs">Live scanning</div></div>
<div class="flow-arrow text-blue-500 text-2xl" data-step="5">→</div>
<div class="flow-step glass-card p-4 rounded-xl text-center w-32" data-step="6">
<i data-lucide="alert-circle" class="w-8 h-8 text-red-400 mx-auto mb-2"></i>
<div class="text-white text-sm font-semibold">Alert</div>
<div class="text-slate-500 text-xs">Violation found</div></div>
<div class="flow-arrow text-blue-500 text-2xl" data-step="7">→</div>
<div class="flow-step glass-card p-4 rounded-xl text-center w-32" data-step="8">
<i data-lucide="layout-dashboard" class="w-8 h-8 text-green-400 mx-auto mb-2"></i>
<div class="text-white text-sm font-semibold">Dashboard</div>
<div class="text-slate-500 text-xs">Full visibility</div></div>
</div>
<div class="mt-8 glass-card inline-flex items-center gap-3 px-5 py-3 rounded-full">
<i data-lucide="zap" class="w-4 h-4 text-blue-400"></i>
<span class="text-slate-300 text-sm">End-to-end in <span class="text-blue-400 font-mono">under 60 seconds</span></span>
</div></div></div></div>'''

SLIDE7_ARCH = '''<div class="slide" id="slide6">
<div class="absolute inset-0 bg-navy-900"></div>
<div class="orb w-64 h-64 bg-blue-600/20 top-20 right-20"></div>
<div class="relative z-10 flex flex-col justify-center h-full px-16 md:px-24">
<div class="max-w-6xl mx-auto w-full">
<div class="flex items-center gap-3 mb-6">
<span class="text-purple-500 font-mono text-sm">06</span>
<div class="h-px flex-1 bg-gradient-to-r from-purple-500/50 to-transparent"></div>
<span class="text-purple-400 text-sm font-medium uppercase tracking-wider">System Architecture</span>
</div>
<h2 class="font-display font-bold text-4xl md:text-5xl mb-2 text-center">Built for <span class="text-purple-400">Scale</span> &amp; <span class="text-purple-400">Security</span></h2>
<p class="sub-explain text-center mb-8">A modular, enterprise-grade system designed to handle millions of records.</p>
<div class="glass-card p-6 rounded-2xl">
<div class="grid md:grid-cols-3 gap-6">
<div class="text-center">
<div class="w-full h-28 rounded-xl bg-gradient-to-br from-blue-600/20 to-blue-800/20 border border-blue-500/30 flex flex-col items-center justify-center mb-3"><i data-lucide="layout" class="w-8 h-8 text-blue-400 mb-1"></i><span class="text-sm font-semibold text-blue-300">Frontend</span></div>
<p class="sub-explain text-xs">Interactive dashboard for compliance teams</p>
<div class="space-y-1 text-xs text-slate-400 mt-2"><div class="bg-slate-800/50 rounded px-2 py-1">React + Tailwind</div><div class="bg-slate-800/50 rounded px-2 py-1">SPA Architecture</div></div>
</div>
<div class="text-center">
<div class="w-full h-28 rounded-xl bg-gradient-to-br from-purple-600/20 to-purple-800/20 border border-purple-500/30 flex flex-col items-center justify-center mb-3"><i data-lucide="server" class="w-8 h-8 text-purple-400 mb-1"></i><span class="text-sm font-semibold text-purple-300">API Layer</span></div>
<p class="sub-explain text-xs">Handles all requests and business logic</p>
<div class="space-y-1 text-xs text-slate-400 mt-2"><div class="bg-slate-800/50 rounded px-2 py-1">FastAPI (Python)</div><div class="bg-slate-800/50 rounded px-2 py-1">JWT Auth + RBAC</div></div>
</div>
<div class="text-center">
<div class="w-full h-28 rounded-xl bg-gradient-to-br from-green-600/20 to-green-800/20 border border-green-500/30 flex flex-col items-center justify-center mb-3"><i data-lucide="cpu" class="w-8 h-8 text-green-400 mb-1"></i><span class="text-sm font-semibold text-green-300">AI Engine</span></div>
<p class="sub-explain text-xs">Reads policies and generates compliance rules</p>
<div class="space-y-1 text-xs text-slate-400 mt-2"><div class="bg-slate-800/50 rounded px-2 py-1">Fine-tuned LLM + RAG</div><div class="bg-slate-800/50 rounded px-2 py-1">Rule-to-SQL Compiler</div></div>
</div></div>
<div class="mt-6 pt-6 border-t border-slate-700">
<div class="flex items-center justify-center gap-4 mb-3"><i data-lucide="database" class="w-5 h-5 text-slate-400"></i><span class="text-sm font-medium text-slate-300">Data Layer</span></div>
<div class="flex justify-center gap-3"><div class="glass-card px-3 py-1.5 rounded-lg text-xs text-slate-400">PostgreSQL</div><div class="glass-card px-3 py-1.5 rounded-lg text-xs text-slate-400">Redis</div><div class="glass-card px-3 py-1.5 rounded-lg text-xs text-slate-400">Vector DB</div><div class="glass-card px-3 py-1.5 rounded-lg text-xs text-slate-400">S3</div></div>
</div></div>
<div class="mt-4 flex justify-center gap-6 text-xs text-slate-500">
<span class="flex items-center gap-1"><i data-lucide="lock" class="w-3 h-3"></i> SOC 2</span>
<span class="flex items-center gap-1"><i data-lucide="shield" class="w-3 h-3"></i> Read-Only Access</span>
<span class="flex items-center gap-1"><i data-lucide="eye" class="w-3 h-3"></i> Explainable AI</span>
</div></div></div></div>'''

SLIDE8_MVP = '''<div class="slide" id="slide7">
<div class="absolute inset-0 bg-gradient-to-br from-navy-900 to-navy-800"></div>
<div class="orb w-80 h-80 bg-blue-600/15 top-0 right-0"></div>
<div class="relative z-10 flex flex-col justify-center h-full px-16 md:px-24">
<div class="max-w-6xl mx-auto w-full">
<div class="flex items-center gap-3 mb-8">
<span class="text-green-500 font-mono text-sm">07</span>
<div class="h-px flex-1 bg-gradient-to-r from-green-500/50 to-transparent"></div>
<span class="text-green-400 text-sm font-medium uppercase tracking-wider">Live MVP</span>
</div>
<div class="grid md:grid-cols-2 gap-12 items-center">
<div>
<h2 class="font-display font-bold text-5xl mb-4">See it in <span class="text-green-400">action</span></h2>
<p class="sub-explain mb-6">Every feature you see is working code, built during this hackathon.</p>
<div class="space-y-4">
<div class="flex items-center gap-3 text-slate-300"><i data-lucide="file-up" class="w-5 h-5 text-green-400"></i><span>PDF Upload &amp; AI Extraction</span></div>
<div class="flex items-center gap-3 text-slate-300"><i data-lucide="activity" class="w-5 h-5 text-green-400"></i><span>Real-time Violation Detection</span></div>
<div class="flex items-center gap-3 text-slate-300"><i data-lucide="users" class="w-5 h-5 text-green-400"></i><span>Human-in-the-Loop Review</span></div>
<div class="flex items-center gap-3 text-slate-300"><i data-lucide="file-bar-chart" class="w-5 h-5 text-green-400"></i><span>Audit-ready Reports</span></div>
</div>
<div class="mt-6 p-3 bg-green-500/10 border border-green-500/20 rounded-xl flex items-center gap-3">
<i data-lucide="code" class="w-5 h-5 text-green-400"></i>
<span class="text-green-400 font-mono text-sm">65,000+ lines of code</span>
</div></div>
<div class="glass-card p-4 rounded-2xl shadow-2xl">
<div class="bg-navy-900 rounded-xl overflow-hidden border border-slate-800">
<div class="flex items-center gap-2 px-4 py-3 border-b border-slate-800 bg-slate-800/50">
<div class="flex gap-1.5"><div class="w-2.5 h-2.5 rounded-full bg-red-500/50"></div><div class="w-2.5 h-2.5 rounded-full bg-yellow-500/50"></div><div class="w-2.5 h-2.5 rounded-full bg-green-500/50"></div></div>
<div class="flex-1 text-center text-[10px] text-slate-500 font-mono">app.complyr.ai/dashboard</div>
</div>
<div class="p-4 space-y-3">
<div class="grid grid-cols-3 gap-2">
<div class="bg-slate-800/50 p-2 rounded border border-slate-700"><div class="text-[10px] text-slate-500 uppercase">Policies</div><div class="text-lg font-bold text-white">2</div></div>
<div class="bg-slate-800/50 p-2 rounded border border-slate-700"><div class="text-[10px] text-slate-500 uppercase">Violations</div><div class="text-lg font-bold text-red-400">8</div></div>
<div class="bg-slate-800/50 p-2 rounded border border-slate-700"><div class="text-[10px] text-slate-500 uppercase">Score</div><div class="text-lg font-bold text-green-400">A+</div></div>
</div>
<div class="h-24 bg-slate-800/30 rounded flex items-end justify-between px-2 pb-2 gap-1">
<div class="flex-1 bg-blue-500/60 rounded-t-sm" style="height:40%"></div>
<div class="flex-1 bg-blue-500/60 rounded-t-sm" style="height:65%"></div>
<div class="flex-1 bg-blue-500/60 rounded-t-sm" style="height:45%"></div>
<div class="flex-1 bg-blue-500/60 rounded-t-sm" style="height:80%"></div>
<div class="flex-1 bg-blue-500/60 rounded-t-sm" style="height:55%"></div>
<div class="flex-1 bg-blue-500/60 rounded-t-sm" style="height:90%"></div>
<div class="flex-1 bg-blue-500/60 rounded-t-sm" style="height:70%"></div>
</div>
<div class="flex items-center gap-2 text-xs text-slate-400"><span class="w-2 h-2 rounded-full bg-red-500 animate-pulse"></span>Live monitoring active</div>
</div></div></div></div></div></div></div>'''

SLIDE9_TECH = '''<div class="slide" id="slide8">
<div class="absolute inset-0 bg-navy-900"></div>
<div class="orb w-96 h-96 bg-indigo-600/20 bottom-0 left-0"></div>
<div class="relative z-10 flex flex-col justify-center h-full px-16 md:px-24">
<div class="max-w-5xl mx-auto w-full">
<div class="flex items-center gap-3 mb-6">
<span class="text-indigo-500 font-mono text-sm">08</span>
<div class="h-px flex-1 bg-gradient-to-r from-indigo-500/50 to-transparent"></div>
<span class="text-indigo-400 text-sm font-medium uppercase tracking-wider">Technology Stack</span>
</div>
<h2 class="font-display font-bold text-4xl md:text-5xl mb-10 text-center">Modern. <span class="text-indigo-400">Fast.</span> Scalable.</h2>
<div class="grid grid-cols-2 md:grid-cols-4 gap-4">
<div class="tech-card glass-card p-4 rounded-xl border border-slate-700/50 transition-all duration-300"><div class="w-10 h-10 rounded-lg bg-blue-500/20 flex items-center justify-center mb-3 border border-blue-500/30"><span class="text-blue-400 font-bold text-sm">R</span></div><div class="text-white font-semibold text-sm mb-1">React</div><div class="text-slate-500 text-xs">Frontend</div></div>
<div class="tech-card glass-card p-4 rounded-xl border border-slate-700/50 transition-all duration-300"><div class="w-10 h-10 rounded-lg bg-cyan-500/20 flex items-center justify-center mb-3 border border-cyan-500/30"><span class="text-cyan-400 font-bold text-sm">T</span></div><div class="text-white font-semibold text-sm mb-1">Tailwind</div><div class="text-slate-500 text-xs">Styling</div></div>
<div class="tech-card glass-card p-4 rounded-xl border border-slate-700/50 transition-all duration-300"><div class="w-10 h-10 rounded-lg bg-green-500/20 flex items-center justify-center mb-3 border border-green-500/30"><span class="text-green-400 font-bold text-sm">F</span></div><div class="text-white font-semibold text-sm mb-1">FastAPI</div><div class="text-slate-500 text-xs">Backend</div></div>
<div class="tech-card glass-card p-4 rounded-xl border border-slate-700/50 transition-all duration-300"><div class="w-10 h-10 rounded-lg bg-blue-500/20 flex items-center justify-center mb-3 border border-blue-500/30"><span class="text-blue-400 font-bold text-sm">P</span></div><div class="text-white font-semibold text-sm mb-1">PostgreSQL</div><div class="text-slate-500 text-xs">Database</div></div>
<div class="tech-card glass-card p-4 rounded-xl border border-slate-700/50 transition-all duration-300"><div class="w-10 h-10 rounded-lg bg-red-500/20 flex items-center justify-center mb-3 border border-red-500/30"><span class="text-red-400 font-bold text-sm">R</span></div><div class="text-white font-semibold text-sm mb-1">Redis</div><div class="text-slate-500 text-xs">Cache</div></div>
<div class="tech-card glass-card p-4 rounded-xl border border-slate-700/50 transition-all duration-300"><div class="w-10 h-10 rounded-lg bg-purple-500/20 flex items-center justify-center mb-3 border border-purple-500/30"><span class="text-purple-400 font-bold text-sm">AI</span></div><div class="text-white font-semibold text-sm mb-1">GPT-4</div><div class="text-slate-500 text-xs">LLM</div></div>
<div class="tech-card glass-card p-4 rounded-xl border border-slate-700/50 transition-all duration-300"><div class="w-10 h-10 rounded-lg bg-blue-500/20 flex items-center justify-center mb-3 border border-blue-500/30"><span class="text-blue-400 font-bold text-sm">D</span></div><div class="text-white font-semibold text-sm mb-1">Docker</div><div class="text-slate-500 text-xs">Deploy</div></div>
<div class="tech-card glass-card p-4 rounded-xl border border-slate-700/50 transition-all duration-300"><div class="w-10 h-10 rounded-lg bg-orange-500/20 flex items-center justify-center mb-3 border border-orange-500/30"><span class="text-orange-400 font-bold text-sm">A</span></div><div class="text-white font-semibold text-sm mb-1">AWS</div><div class="text-slate-500 text-xs">Cloud</div></div>
</div>
<div class="mt-6 glass-card p-3 rounded-xl"><div class="flex items-center justify-between text-sm"><span class="text-slate-400">Architecture</span><span class="text-white font-medium">Microservices + Event-Driven</span></div></div>
</div></div></div>'''

SLIDE10_IMPACT = '''<div class="slide" id="slide9">
<div class="absolute inset-0 bg-gradient-to-br from-navy-900 via-navy-800 to-navy-900"></div>
<div class="orb w-64 h-64 bg-green-600/20 top-10 left-10"></div>
<div class="orb w-48 h-48 bg-blue-600/20 bottom-10 right-10" style="animation-delay:-3s"></div>
<div class="relative z-10 flex flex-col justify-center h-full px-16 md:px-24">
<div class="max-w-5xl mx-auto w-full text-center">
<div class="flex items-center justify-center gap-3 mb-6">
<span class="text-green-500 font-mono text-sm">09</span>
<span class="text-green-400 text-sm font-medium uppercase tracking-wider">Impact</span>
</div>
<h2 class="font-display font-bold text-5xl md:text-6xl mb-4">Numbers that <span class="text-green-400">matter</span></h2>
<p class="sub-explain mb-12">Measurable results from day one of deployment.</p>
<div class="grid md:grid-cols-3 gap-8">
<div class="glass-card p-8 rounded-2xl glow-stat animate-slide-up">
<div class="text-6xl font-black text-green-400 mb-2"><span class="counter" data-target="95">0</span>%</div>
<div class="text-white font-semibold mb-1">Time Reduction</div>
<div class="text-slate-400 text-sm">From weeks to minutes</div>
</div>
<div class="glass-card p-8 rounded-2xl glow-stat animate-slide-up" style="animation-delay:0.15s">
<div class="text-6xl font-black text-blue-400 mb-2">24/7</div>
<div class="text-white font-semibold mb-1">Continuous Monitoring</div>
<div class="text-slate-400 text-sm">Never miss a violation</div>
</div>
<div class="glass-card p-8 rounded-2xl glow-stat animate-slide-up" style="animation-delay:0.3s">
<div class="text-6xl font-black text-purple-400 mb-2">₹<span class="counter" data-target="2">0</span>Cr+</div>
<div class="text-white font-semibold mb-1">Avg. Penalty Avoided</div>
<div class="text-slate-400 text-sm">Per detected violation</div>
</div>
</div>
<div class="grid md:grid-cols-3 gap-4 mt-6">
<div class="glass-card p-4 rounded-xl text-center"><div class="text-2xl font-bold text-blue-400"><span class="counter" data-target="1200">0</span>+</div><div class="text-slate-400 text-xs">Rules Extracted</div></div>
<div class="glass-card p-4 rounded-xl text-center"><div class="text-2xl font-bold text-red-400"><span class="counter" data-target="340">0</span>+</div><div class="text-slate-400 text-xs">Violations Detected</div></div>
<div class="glass-card p-4 rounded-xl text-center"><div class="text-2xl font-bold text-green-400"><span class="counter" data-target="98">0</span>%</div><div class="text-slate-400 text-xs">Risk Score Accuracy</div></div>
</div>
<div class="mt-8 glass-card inline-flex items-center gap-4 px-6 py-3 rounded-full">
<i data-lucide="trending-up" class="w-5 h-5 text-green-400"></i>
<span class="text-slate-300">ROI realized in <span class="text-white font-semibold">first month</span></span>
</div></div></div></div>'''

SLIDE11_CTA = '''<div class="slide" id="slide10">
<div class="absolute inset-0 bg-gradient-to-br from-navy-900 via-blue-900/30 to-navy-900"></div>
<div class="orb w-96 h-96 bg-blue-600/30 top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2"></div>
<div class="relative z-10 flex flex-col items-center justify-center h-full px-8 text-center">
<div class="animate-fade-in">
<div class="w-20 h-20 bg-gradient-to-br from-blue-500 to-blue-700 rounded-2xl flex items-center justify-center mx-auto mb-8 shadow-2xl shadow-blue-500/40"><i data-lucide="shield-check" class="w-10 h-10 text-white"></i></div>
<h1 class="font-display font-black text-6xl md:text-7xl mb-6"><span class="text-gradient">Complyr</span></h1>
<p class="text-2xl text-slate-300 mb-2 max-w-2xl mx-auto">The autonomous compliance layer for regulated industries</p>
<p class="sub-explain mb-8">Designed for Indian and global enterprises</p>
<div class="tricolor-bar w-48 mx-auto mb-8"></div>
<div class="flex flex-col md:flex-row gap-4 justify-center items-center">
<div class="glass-card px-6 py-3 rounded-full flex items-center gap-3"><i data-lucide="user" class="w-5 h-5 text-blue-400"></i><span class="text-slate-300 text-sm">Shubham Jha</span></div>
<div class="glass-card px-6 py-3 rounded-full flex items-center gap-3"><i data-lucide="user" class="w-5 h-5 text-blue-400"></i><span class="text-slate-300 text-sm">Shreekant Bharti</span></div>
<div class="glass-card px-6 py-3 rounded-full flex items-center gap-3"><i data-lucide="user" class="w-5 h-5 text-blue-400"></i><span class="text-slate-300 text-sm">Shrishti</span></div>
</div>
<div class="mt-12 text-slate-500 text-sm"><p>Built with \U0001f499 BeyondInfinity</p></div>
</div></div></div>'''

SCRIPT = '''<script>
let currentSlide=0;const totalSlides=''' + str(TOTAL) + ''';
function animateCounters(){document.querySelectorAll('.slide.active .counter').forEach(el=>{const target=parseInt(el.dataset.target);const duration=2000;const step=target/(duration/16);let current=0;const timer=setInterval(()=>{current+=step;if(current>=target){el.textContent=target;clearInterval(timer)}else{el.textContent=Math.floor(current)}},16)})}
function animateFlow(){const flow=document.getElementById('flowDiagram');if(!flow)return;const items=flow.querySelectorAll('[data-step]');items.forEach(item=>{item.classList.remove('visible')});items.forEach((item,i)=>{setTimeout(()=>{item.classList.add('visible')},i*300)})}
function updateSlide(){document.querySelectorAll('.slide').forEach((s,i)=>{s.classList.remove('active');if(i===currentSlide)s.classList.add('active')});document.querySelectorAll('.nav-dot').forEach((d,i)=>{d.classList.toggle('active',i===currentSlide)});document.getElementById('progressBar').style.width=((currentSlide+1)/totalSlides)*100+'%';lucide.createIcons();animateCounters();animateFlow()}
function nextSlide(){if(currentSlide<totalSlides-1){currentSlide++;updateSlide()}}
function prevSlide(){if(currentSlide>0){currentSlide--;updateSlide()}}
function goToSlide(n){currentSlide=n;updateSlide()}
document.addEventListener('keydown',e=>{if(e.key==='ArrowRight'||e.key===' '){e.preventDefault();nextSlide()}else if(e.key==='ArrowLeft'){e.preventDefault();prevSlide()}else if(e.key==='Home'){e.preventDefault();goToSlide(0)}else if(e.key==='End'){e.preventDefault();goToSlide(totalSlides-1)}});
let tx=0,te=0;document.addEventListener('touchstart',e=>{tx=e.changedTouches[0].screenX});document.addEventListener('touchend',e=>{te=e.changedTouches[0].screenX;if(tx-te>50)nextSlide();else if(te-tx>50)prevSlide()});
document.addEventListener('DOMContentLoaded',()=>{lucide.createIcons();updateSlide()});
</script>'''

FOOTER = '</body>\n</html>'

# Assemble and write
html = HEAD + nav_dots() + SLIDE1 + SLIDE2 + SLIDE3_GAP + SLIDE4_COMPARE + SLIDE5_SOLUTION + SLIDE6_FLOW + SLIDE7_ARCH + SLIDE8_MVP + SLIDE9_TECH + SLIDE10_IMPACT + SLIDE11_CTA + SCRIPT + FOOTER

with open(r'c:\Users\jhak8\Desktop\hackfest\new.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f"✅ Enhanced deck generated: {len(html):,} chars, {TOTAL} slides")
