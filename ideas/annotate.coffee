cheerio = require 'cheerio'
fs = require 'fs'

input = fs.readFileSync 'data/article.html', 'utf-8'
root = cheerio.load input

ps = root 'p'
lines = []
ps.each (i, p) ->
  lines.push cheerio(p).text()
fs.writeFileSync 'input.txt', lines.join '\n'
