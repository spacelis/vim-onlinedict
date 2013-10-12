if exists("g:loaded_online_dictionaries")
    finish
endif
let g:loaded_online_thesaurus = 1

"---Initialize--------------------------------{{{1
if !exists('s:onlinedict_did_init')
    let s:script_path = expand("<sfile>:p")
    let s:script_dir = expand("<sfile>:p:h")
    let s:pylib_dir = fnamemodify(s:script_dir, ':p:h:h') . '/pylib'
python << EOF
import sys, vim, os
if not vim.eval("s:pylib_dir") in sys.path:
    sys.path.append(vim.eval("s:pylib_dir"))
from connectors.dictionaries import OxfordDictionaries
OD = OxfordDictionaries()
EOF
    let s:onlinedict_did_init = 1
endif



let s:save_cpo = &cpo
set cpo&vim

let s:path = expand("<sfile>:p:h")

function! s:Lookup(word)
    silent keepalt belowright split thesaurus
    setlocal noswapfile nobuflisted nospell nowrap modifiable
    setlocal buftype=nofile bufhidden=hide
    1,$d
py<<EOF
page = OD.query(vim.eval('a:word'))
vim.current.buffer[:] = page.split('\n')
EOF
    normal! Vgqgg
    exec 'resize ' . (line('$'))
    setlocal nomodifiable filetype=thesaurus
    nnoremap <silent> <buffer> q :q<CR>
endfunction

if !exists('g:online_dictionaries_map_keys')
    let g:online_dictionaries_map_keys = 1
endif

if g:online_dictionaries_map_keys
    nnoremap <unique> -K :OnlineDictionariesCurrentWord<CR>
endif

command! OnlineDictionariesCurrentWord :call <SID>Lookup(expand('<cword>'))
command! OnlineDictionariesLookup :call <SID>Lookup(expand('<cword>'))
command! -nargs=1 Dictionaries :call <SID>Lookup(<f-args>)

let &cpo = s:save_cpo