execute pathogen#infect()
syntax on

set ruler

set ignorecase

set textwidth=80

set nocompatible

set backspace=indent,eol,start

set showcmd

" indent
set autoindent
set shiftwidth=4
set softtabstop=4
set expandtab

" on a search go case sensitive!
set smartcase

" show line numbers
set number

" enable mouse
"set mouse=a

" increment search
set incsearch

" highlight search
set hlsearch

" when press N or n it will go to the next word found 
" and centralize
map N Nzz
map n Nzz
map p ]p
map ; :
map ´ gg=G
"map zz ZZ
"map q :q!<Enter>
"map Q q

" well, you know what it means 
""inoremap ( ()
"inoremap { {}
""inoremap yy <Esc>yy
" inoremap dd <Esc>dd

" detect the filetype 
filetype on
filetype indent on
filetype plugin on
