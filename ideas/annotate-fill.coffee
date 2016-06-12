cheerio = require 'cheerio'
fs = require 'fs'

input = fs.readFileSync 'data/article.html', 'utf-8'
output = fs.readFileSync 'output.txt', 'utf-8'
root = cheerio.load input

lines = output.split '\n'

ps = root 'p'
ps.each (i, p) ->
  p = cheerio(p)
  words = ("<span style='color:black;opacity:1'>#{word}</span>"for word in lines[i].split())
  p.html(words.join ' ')

fs.writeFileSync 'out.html', root.html()
