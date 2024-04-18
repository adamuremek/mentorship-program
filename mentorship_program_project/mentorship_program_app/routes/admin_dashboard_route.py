"""
/*********************************************************************/
/* FILE NAME: admin_dashboard_routes.py                                     */
/*********************************************************************/
/* PART OF PROJECT: Mentorship Program                               */
/*********************************************************************/
/* WRITTEN BY: Andrew P and Jordan                                   */
/* (OFFICIAL) DATE CREATED: Long ago                                 */
/*********************************************************************/
/* PROJECT PURPOSE:                                                  */
/*                                                                   */
/* This project aims to facilitate the connection between SVSU CSIS  */
/* students and experienced mentors in the industry through an       */
/* interactive web-based platform.                                   */
/*********************************************************************/
/* FILE PURPOSE:                                                     */
/*                                                                   */
/* This file contains the server-side logic necessary for rendering  */
/* the administrative dashboard. This includes compiling statistics  */
/* about mentors and mentees, as well as providing a high-level view */
/* of program activities.                                            */
/*********************************************************************/
/* DJANGO IMPORTED VARIABLE LIST (Alphabetically):                   */
/*                                                                   */
/* - HttpResponse: Class for sending HTTP responses                  */
/* - HttpRequest: Class for handling HTTP requests                   */
/* - loader: Module to load Django templates                         */
/*********************************************************************/
/* MODIFICATION HISTORY:                                             */
/*********************************************************************/
/* Date       | Changed By | Changes Made                            */
/* -----------|------------|---------------------------------------- */

/*********************************************************************/

"""

from django.http import HttpResponse
from django.template import loader
from mentorship_program_app.models import *
from .reporting import get_project_overall_statistics, get_project_time_statistics
from .emails import *
from ..models import *

def admin_dashboard(req):
    """
    Renders the administrative dashboard with comprehensive statistics on the mentorship program.

    Parameters:
    - req : HttpRequest: HTTP request object used to generate the HTTP response.

    Returns:
    - HttpResponse: Rendered HTML for the admin dashboard.

    This function gathers various statistics about active and inactive mentees and mentors, 
    categorizes them by daily, weekly, monthly, and lifetime intervals, and displays them
    on the admin dashboard for a comprehensive overview.
    """
    template = loader.get_template('admin_dashboard.html')
    

    overall_stats = get_project_overall_statistics()
    timespan_stats = get_project_time_statistics()

    interests = Interest.objects.all().order_by('id')

    context = {
               "active_mentees"              : overall_stats["active_mentees"              ],
               "assigned_mentees"            : overall_stats["assigned_mentees"            ],
               "unassigned_mentees"          : overall_stats["unassigned_mentees"          ],
               "inactive_mentees"            : overall_stats["inactive_mentees"            ],
               "active_mentors"              : overall_stats["active_mentors"              ],
               "assigned_mentors"            : overall_stats["assigned_mentors"            ],
               "unassigned_mentors"          : overall_stats["unassigned_mentors"          ],
               "inactive_mentors"            : overall_stats["inactive_mentors"            ],
               "mentees_per_mentor"          : overall_stats["mentees_per_mentor"          ],
               "mentor_retention_rate"       : overall_stats["mentor_retention_rate"       ],
               "successful_match_rate"       : overall_stats["successful_match_rate"       ],
               "pending_mentors"             : overall_stats["pending_mentors"             ],
               "unresolved_reports"          : overall_stats["unresolved_reports"          ],
               "interests"                   : interests,
               
               # Daily
               "daily_visitors"                  : timespan_stats["Daily"][0],
               "daily_mentee_signup"             : timespan_stats["Daily"][1],
               "daily_mentor_signup"             : timespan_stats["Daily"][2],
               "daily_assigned_mentees"          : timespan_stats["Daily"][3],
               "daily_deactivate_mentees"        : timespan_stats["Daily"][4],
               "daily_deactivate_mentors"        : timespan_stats["Daily"][5],
               "daily_terminated_mentorships"    : timespan_stats["Daily"][6],

               # Week
               "weekly_visitors"                 : timespan_stats["Weekly"][0],
               "weekly_mentee_signup"            : timespan_stats["Weekly"][1],
               "weekly_mentor_signup"            : timespan_stats["Weekly"][2],
               "weekly_assigned_mentees"         : timespan_stats["Weekly"][3],
               "weekly_deactivate_mentees"       : timespan_stats["Weekly"][4],
               "weekly_deactivate_mentors"       : timespan_stats["Weekly"][5],
               "weekly_terminated_mentorships"   : timespan_stats["Weekly"][6],
               
               # Month
               "monthly_visitors"                : timespan_stats["Monthly"][0],
               "monthly_mentee_signup"           : timespan_stats["Monthly"][1],
               "monthly_mentor_signup"           : timespan_stats["Monthly"][2],
               "monthly_assigned_mentees"        : timespan_stats["Monthly"][3],
               "monthly_deactivate_mentees"      : timespan_stats["Monthly"][4],
               "monthly_deactivate_mentors"      : timespan_stats["Monthly"][5],
               "monthly_terminated_mentorships"  : timespan_stats["Monthly"][6],
               
               # Lifetime
               "lifetime_visitors"               : timespan_stats["Lifetime"][0],
               "lifetime_mentee_signup"          : timespan_stats["Lifetime"][1],
               "lifetime_mentor_signup"          : timespan_stats["Lifetime"][2],
               "lifetime_assigned_mentees"       : timespan_stats["Lifetime"][3],
               "lifetime_deactivate_mentees"     : timespan_stats["Lifetime"][4],
               "lifetime_deactivate_mentors"     : timespan_stats["Lifetime"][5],
               "lifetime_terminated_mentorships" : timespan_stats["Lifetime"][6],
               
            }
    return HttpResponse(template.render(context, req))