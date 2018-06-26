#!/usr/local/bin/env python3
# -*- coding:utf-8 -*-
# __author__:"Howard"


class Page:
    def __init__(self, data_list, current_pag, num_per_pag=20, display_pagination_num=5):
        self.data_list = data_list
        self.current_pag = current_pag
        self.num_per_pag = num_per_pag
        self.display_pagination_num = display_pagination_num
        self.data = self.data_list[(self.current_pag-1)*self.num_per_pag: self.num_per_pag*self.current_pag]

    @property
    def pag_count(self):
        pag_count, y = divmod(len(self.data_list), self.num_per_pag)
        if y:
            pag_count += 1
        return pag_count

    def pagination_str(self, base_url):
        p_url = []
        if self.current_pag == 1:
            prev_pag = '<a class="pag" href="javascript:void(0);">上一页</a>'
        else:
            prev_pag = '<a class="pag" href="/?p=%s">上一页</a>' % (self.current_pag - 1)
        p_url.append(prev_pag)
        if self.pag_count < self.display_pagination_num:
            start_index = 1
            end_index = self.pag_count
        else:
            if self.current_pag <= (self.display_pagination_num-1)/2+1:
                start_index = 1
                end_index = self.display_pagination_num+1
            elif self.pag_count - self.current_pag <= (self.display_pagination_num-1)/2:
                start_index = self.pag_count - self.display_pagination_num + 1
                end_index = self.pag_count + 1
            else:
                start_index = self.current_pag - (self.display_pagination_num-1)/2
                end_index = self.current_pag + (self.display_pagination_num-1)/2 + 1
        for p1 in range(int(start_index), int(end_index)):
            if p1 == self.current_pag:
                p_url_tmp = '<a class="pag active" href="%s?p=%s">%s</a>' % (base_url, p1, p1)
            else:
                p_url_tmp = '<a class="pag" href="%s?p=%s">%s</a>' % (base_url, p1, p1)
            p_url.append(p_url_tmp)
        if self.current_pag == self.pag_count:
            next_pag = '<a class="pag" href="javascript:void(0);">下一页</a>'
        else:
            next_pag = '<a class="pag" href="%s?p=%s">下一页</a>' % (base_url, self.current_pag + 1)
        p_url.append(next_pag)
        jump = """
        <input type="text"/><a id='jump' onclick='jumpTo(this,"%s?p=");'>go</a>
        <script>
            function jumpTo(ths, base_url){
                var v = ths.previousElementSibling.value;
                jump_url = base_url+v;
                location.href = jump_url;
            }
        </script>
        """ % base_url
        p_url.append(jump)
        p_str = ''.join(p_url)
        return p_str
