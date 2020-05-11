diff --git a/source/index.rst b/source/index.rst
index aa701c3..7c994ec 100644
--- a/source/index.rst
+++ b/source/index.rst
@@ -1,40 +1,42 @@
 Django Views — The Right Way
 ============================
 
 Welcome to my opinionated guide on how to write views in Django!
 
 **WORK IN PROGRESS** - this is an early draft, you should probably come back
  later...
 
-This guide was inspired by the fact that many people on the internet seem to be
-starting with "Class Based Views" (CBVs from now on) as the default way to write
-views, to the point that some are even scared to write "function based views"
-(FBVs), despite the fact that these are so much easier and simpler.
-
-I've also come across various blog posts advising ways to do things that are
-much more complex than necessary, and, perhaps worst of all, some official
-Django documentation which amounts to `well-intentioned advise on how to
-continue the torture of mixins without actually killing yourself
-<https://docs.djangoproject.com/en/dev/topics/class-based-views/mixins/>`_.
-(After a bit of “git blaming” it turns out that I'm `credited
+This guide is the result of my experience in a range of Django and Python
+projects for well over a decade, and the lessons I've learnt.
+
+It has also been prompted by the fact that “Class Based Views” (CBVs from now on)
+seem to have become the default way to teach and learn Django views, to the
+point that some are even scared to write “Function Based Views” (FBVs), despite
+the fact that these are so much easier and simpler.
+
+Perhaps worst of all, some official Django documentation has `well-intentioned
+advise that will help to continue the torture of mixins
+<https://docs.djangoproject.com/en/dev/topics/class-based-views/mixins/>`_ , but
+without actually killing you and putting you out of your misery. (After a bit of
+“git blaming” it turns out that I'm `credited
 <https://github.com/django/django/commit/c4c7fbcc0d9264beb931b45969fc0d8d655c4f83>`_
 in the commit log. I hate it when that happens…)
 
 So, in view of all this, here I am to save the day, and show you The Right Way.
 
 The essential part of this guide is very short, because FBVs are very easy and
 simple. In fact, the `Django tutorial for views
 <https://docs.djangoproject.com/en/3.0/intro/tutorial03/>`_ already has all you
 need to know. Just read that, and skip the bits about CBVs, and you'll be fine.
 
 But if you want a different take on the same things, this guide might be for
-you. I've also added extra bits for common tasks and patterns in FBVs for which
-CBVs are often suggested as the solution. If you read all of it:
+you. I've also gone into significant depth for common tasks and patterns in FBVs
+for which CBVs are often suggested as the solution. If you read all of it:
 
 * You'll learn how to make your views usually shorter and definitely much
   simpler than if you used CBVs.
 * You'll be freed from learning a whole stack of terrifying APIs that were only
   making your life harder (and teaching you bad patterns).
 * Instead of learning a bunch of Django specific APIs, you will gain much more
   re-usable knowledge:
 
