import fastJsonPatch from 'fast-json-patch'
import fs from 'fs'

const rawHistory = JSON.parse(fs.readFileSync('./metamask-vault-history.json', 'utf8'))

// determine array-like length
rawHistory.length = Object.keys(rawHistory).map(Number).reduce((a,b)=>Math.max(a,b))

// sanitized history, oldest to newest
const history = Array.from(rawHistory).filter(Boolean)

// console.log(rawHistory)
// console.log(history)

history.reduce((a,b,index) => {
  const patchSet = fastJsonPatch.compare(a,b)
  visitTransition(index, patchSet)
  return b
})

function visitTransition (index, rawPatchSet) {
  const cleanPatchSet = rawPatchSet.filter(filterPatch)
  if (!cleanPatchSet.length) return
  console.log(index, JSON.stringify(cleanPatchSet, null, 2))
}

function filterPatch (patch) {
  // only filter certain value updates
  if (patch.op !== 'replace') {
    return true
  }
  // 
  if (
    patch.path.startsWith('CurrencyController/conversionDate')
    || patch.path.startsWith('CurrencyController/conversionRate')
    || patch.path.startsWith('CurrencyController/usdConversionRate')
  ) return false
}