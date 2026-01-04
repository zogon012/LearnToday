function parseCSV(text){
  const lines = text.trim().split(/\r?\n/).filter(Boolean)
  const headers = lines.shift().split(',').map(h=>h.trim())
  return lines.map(line=>{
    const cols = line.split(',')
    const obj = {}
    headers.forEach((h,i)=> obj[h]=cols[i] ? cols[i].trim() : '')
    return obj
  })
}

function formatDate(dstr){
  // input yyyy-mm-dd -> yyyy년 m월 d일 (weekday)
  try{
    const [y,m,d]=dstr.split('-').map(Number)
    const dt=new Date(y,m-1,d)
    return dt.toLocaleDateString('ko-KR',{year:'numeric',month:'long',day:'numeric',weekday:'short'})
  }catch(e){return dstr}
}

function buildUI(matches){
  const container=document.getElementById('container')
  container.innerHTML=''
  // group by date
  const byDate = {}
  matches.forEach(m=>{
    (byDate[m.date]||(byDate[m.date]=[])).push(m)
  })
  const dates = Object.keys(byDate).sort()
  dates.forEach(date=>{
    const dayBlock=document.createElement('section')
    dayBlock.className='day-block'
    const dh=document.createElement('div')
    dh.className='date-header'
    // render plain formatted date for all dates (no special decoration)
    dh.textContent = formatDate(date)
    dayBlock.appendChild(dh)

    byDate[date].sort((a,b)=> a.time.localeCompare(b.time)).forEach(m=>{
      const card=document.createElement('article')
      card.className='match-card'
      // data attributes for team-list parsing
      card.dataset.date = m.date || ''
      card.dataset.time = m.time || ''
      card.dataset.home = m.home || ''
      card.dataset.away = m.away || ''
      card.dataset.stadium = m.stadium || ''
      const meta=document.createElement('div'); meta.className='meta'
      meta.innerHTML=`<div class="small">${m.time} · ${m.stadium}</div><div class="small">${m.category} · ${m.league} · ${m.match_no}</div>`

      const teams=document.createElement('div'); teams.className='teams'

      const left=document.createElement('div'); left.className='team home'
      left.appendChild(createEmblemElement(m.home))
      const leftName=document.createElement('div'); leftName.className='club'; leftName.textContent = m.home
      left.appendChild(leftName)
      if(String(m.home).includes('김포')) left.classList.add('highlight')

      const right=document.createElement('div'); right.className='team away'
      right.appendChild(createEmblemElement(m.away))
      const rightName=document.createElement('div'); rightName.className='club'; rightName.textContent = m.away
      right.appendChild(rightName)
      if(String(m.away).includes('김포')) right.classList.add('highlight')

      const vs=document.createElement('div'); vs.className='vs'; vs.textContent='vs'

      teams.appendChild(left)
      teams.appendChild(vs)
      teams.appendChild(right)

      card.appendChild(meta)
      card.appendChild(teams)
      dayBlock.appendChild(card)
    })

    container.appendChild(dayBlock)
  })

  // stadium filter removed per UI requirement
}

function createEmblemElement(clubName){
  const wrapper=document.createElement('div')
  wrapper.className='emblem'
  const img=document.createElement('img')
  const safeName = encodeURIComponent(clubName)
  const exts = ['png','svg','jpg','jpeg','webp']
  let idx = 0
  img.alt = clubName
  img.onload = ()=>{}
  img.onerror = ()=>{
    idx++
    if(idx < exts.length){
      img.src = `emblems/${safeName}.${exts[idx]}`
      return
    }
    // fallback: initials
    try{ wrapper.removeChild(img) }catch(e){}
    const initials = clubName.split(/\s+/).map(s=>s[0]||'').join('').slice(0,2)
    const span=document.createElement('div')
    span.className='emblem-fallback'
    span.textContent = initials
    wrapper.appendChild(span)
  }
  img.src = `emblems/${safeName}.${exts[0]}`
  wrapper.appendChild(img)
  return wrapper
}

document.getElementById && (function(){
  const printBtn=document.getElementById('printBtn')
  printBtn.addEventListener('click',()=> window.print())

  fetch('match.csv').then(r=>r.text()).then(t=>{
    const matches = parseCSV(t)
    // expose matches globally for other modules and build team list
    window.matches = matches
    buildUI(matches)
    try{ buildTeamList(matches) }catch(e){}
  }).catch(err=>{
    document.getElementById('container').textContent = 'match.csv를 불러오지 못했습니다. 서버로 정적 파일을 서빙하고 있는지 확인하세요.'
  })
})()

/* ----- Team list & filtering utilities ----- */
function buildTeamList(matches){
  const map = new Map()
  matches.forEach(m=>{
    const home = (m.home||'').trim()
    const away = (m.away||'').trim()
    if(home) map.set(home, (map.get(home)||0)+1)
    if(away) map.set(away, (map.get(away)||0)+1)
  })

  const container = document.getElementById('team-items')
  if(!container) return
  container.innerHTML=''

  const teams = Array.from(map.entries()).sort((a,b)=> b[1]-a[1] || a[0].localeCompare(b[0]))
  teams.forEach(([name,count])=>{
    const li=document.createElement('li'); li.className='team-item'; li.dataset.team=name
    const img=document.createElement('img'); img.className='emblem-sm'; img.alt=name
    const base = `emblems/${encodeURIComponent(name)}`
    img.src = `${base}.png`
    img.onerror = function(){ if(!this._triedSvg){ this._triedSvg=true; this.src=`${base}.svg`} else { const span=createInitialsSpan(name); this.replaceWith(span) }}
    const spanName=document.createElement('span'); spanName.className='tname'; spanName.textContent=name
    const spanCount=document.createElement('span'); spanCount.className='count'; spanCount.textContent=`${count}경기`
    li.appendChild(img); li.appendChild(spanName); li.appendChild(spanCount)
    li.addEventListener('click', ()=>{
      document.querySelectorAll('.team-item.selected').forEach(n=>n.classList.remove('selected'))
      li.classList.add('selected')
      filterByTeam(name)
    })
    container.appendChild(li)
  })

  const search = document.getElementById('team-search')
  search && search.addEventListener('input', (e)=>{
    const q = e.target.value.trim().toLowerCase()
    Array.from(container.children).forEach(ch=>{
      const t = ch.dataset.team.toLowerCase()
      ch.style.display = t.includes(q) ? '' : 'none'
    })
  })
  document.getElementById('team-reset')?.addEventListener('click', ()=>{ document.querySelectorAll('.team-item.selected').forEach(n=>n.classList.remove('selected')); resetFilter() })
}

function createInitialsSpan(name){
  const s=document.createElement('span'); s.className='emblem-sm'; s.style.display='inline-flex'; s.style.alignItems='center'; s.style.justifyContent='center'; s.style.fontSize='12px'; s.style.fontWeight='600'; s.style.background='#f0fbfb'; s.style.color='#0b4b4a'; s.textContent = (name.split(/\s|-/).map(p=>p[0]||'').slice(0,2).join('')).toUpperCase(); return s
}

function filterByTeam(teamName){
  const cards=document.querySelectorAll('.match-card')
  cards.forEach(c=>{
    const txt = (c.textContent||'')
    const shown = txt.includes(teamName)
    if(shown) c.classList.remove('hidden'); else c.classList.add('hidden')
  })
  const first = document.querySelector('.match-card:not(.hidden)')
  if(first) first.scrollIntoView({behavior:'smooth', block:'start'})
}

function resetFilter(){ document.querySelectorAll('.match-card.hidden').forEach(c=>c.classList.remove('hidden')) }

// no toggle: team-list remains static
