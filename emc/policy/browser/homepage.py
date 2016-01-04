#-*- coding: UTF-8 -*-
from five import grok
from plone.memoize.instance import memoize
from zope.component import getMultiAdapter
from Products.CMFCore.interfaces import ISiteRoot
from emc.policy import _
from emc.project.content.project import IProject
from emc.project.content.projectfolder import IProjectFolder

from emc.theme.interfaces import IThemeSpecific


grok.templatedir('templates')

class FrontpageView(grok.View):
     
    grok.context(ISiteRoot)
    grok.template('homepage')
    grok.name('index.html')
    grok.layer(IThemeSpecific)
    grok.require('zope2.View')      

    
    def carouselid(self):
        return "carouselid"
    
    def active(self,i):
        if i == 0:
            return "active"
        else:
            return ""
        
    @memoize
    def carouselresult(self):
        
        out = """
        <div id="carousel-generic" class="carousel slide">
  <!-- Indicators -->
  <ol class="carousel-indicators">
    <li data-target="#carousel-generic" data-slide-to="0" class="active"></li>
    <li data-target="#carousel-generic" data-slide-to="1"></li>
    <li data-target="#carousel-generic" data-slide-to="2"></li>
  </ol>

  <!-- Wrapper for slides -->
  <div class="carousel-inner">
    <div class="item active">
      <img src="http://www.xtshzz.org/xinwenzhongxin/tupianxinwen/xiangtanshishekuaizuzhishoucibishuzhanglianxikuaiyishenglizhaokai/@@images/image/preview" alt="..."/>
      <div class="carousel-caption">
        <h3>大会召开</h3>
      </div>
    </div>
    <div class="item">
      <img src="http://www.xtshzz.org/xinwenzhongxin/tupianxinwen/xiangtanshishekuaizuzhishoucibishuzhanglianxikuaiyishenglizhaokai/@@images/image/preview" alt="..."/>
      <div class="carousel-caption">
        <h3>大会召开</h3>
      </div>
    </div>
    <div class="item">
      <img src="http://www.xtshzz.org/xinwenzhongxin/tupianxinwen/xiangtanshishekuaizuzhishoucibishuzhanglianxikuaiyishenglizhaokai/@@images/image/preview" alt="..."/>
      <div class="carousel-caption">
        <h3>大会召开</h3>
      </div>
    </div>    
  </div>

  <!-- Controls -->
  <a class="left carousel-control" href="#carousel-generic" data-slide="prev">
    <span class="glyphicon glyphicon-chevron-left"></span>
  </a>
  <a class="right carousel-control" href="#carousel-generic" data-slide="next">
    <span class="glyphicon glyphicon-chevron-right"></span>
  </a>

</div>
        """ 
        
        braindata = self.catalog()({'object_provides':Iproject.__identifier__, 
                                    'b_start':0,
                                    'b_size':3,
                             'sort_order': 'reverse',
                             'sort_on': 'created'})
        brainnum = len(braindata)
        if brainnum == 0:return out        

        outhtml = """<div id="%s" class="carousel slide" data-ride="carousel">
        <ol class="carousel-indicators">
        """ % (self.carouselid())
        outhtml2 = '</ol><div class="carousel-inner">'
        for i in range(brainnum):            
            out = """<li data-target='%(carouselid)s' data-slide-to='%(indexnum)s' class='%(active)s'>
            </li>""" % dict(indexnum=str(i),
                    carouselid=''.join(['#',self.carouselid()]),
                    active=self.active(i))
                                               
            outhtml = ''.join([outhtml,out])   # quick concat string
            objurl = braindata[i].getURL()
            linkurl = braindata[i].linkurl
            objtitle = braindata[i].Title
            outimg = """<div class="%(classes)s">
                        <a href="%(linkurl)s"><img width="370" height="227" src="%(imgsrc)s" alt="%(imgtitle)s"/></a>
                          <div class="carousel-caption">
                            <h3>%(imgtitle)s</h3>
                              </div>
                                </div>""" % dict(classes=''.join(["item ", self.active(i)]),
                     linkurl=linkurl,
                     imgsrc=''.join([objurl, "/@@images/image/preview"]),
                     imgtitle=objtitle)
            outhtml2 = ''.join([outhtml2,outimg])   # quick concat string                    
#        outhtml = outhtml +'</ol><div class="carousel-inner">'
        result = ''.join([outhtml,outhtml2])   # quick concat string
        out = """
        </div><a class="left carousel-control" href="%(carouselid)s" data-slide="prev">
    <span class="glyphicon glyphicon-chevron-left"></span>
  </a>
  <a class="right carousel-control" href="%(carouselid)s" data-slide="next">
    <span class="glyphicon glyphicon-chevron-right"></span>
  </a>
</div>""" % dict(carouselid = ''.join(["#", self.carouselid()]))
        return ''.join([result,out])
                
              
# roll zone


        
    def rollheader(self):
        return u"新闻"
    
    def rollmore(self):
        context = self.getOrgnizationFolder()
        return context.absolute_url()


        
# roll table output
    def getProjectFolder(self):
        
        brains = self.catalog()({'object_provides':IProjectFolder.__identifier__})
        context = brains[0].getObject()
        return context        
        
    def getable(self,view):
        """view: a organization folder object's view name
        call view come from my315ok.socialorgnization orgnization_listing module,
        view name may be "orgnizations_administrative","orgnizations_survey"
        """
        context = self.ProjectFolder()
        fview = getMultiAdapter((context,self.request),name=view)
        # call getMemberList function output table
        # fetch 20 items roll
        return fview.getMemberList(start=0,size=20,)
            
