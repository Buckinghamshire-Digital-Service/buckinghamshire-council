from django.conf import settings

from bs4 import BeautifulSoup


def generate_webservice_xml(*args, **kwargs):
    """The name of this function belies the fact that it's just hardcoded for now."""
    xml = (
        """
<webservice type="CaseCreate">
  <name>
   TestCreateComplaints
  </name>
  <urls>
   <url method="POST">"""
        + f"https://groupc.respond.apteancloud.com/Buckinghamshire/ws/case.svc/{settings.RESPOND_COMPLAINTS_WEBSERVICE}"
        + """</url>
  </urls>
  <profiles>
   <profile>
    Service Users
   </profile>
  </profiles>
  <fields>
   <field data-type="SystemAllocation" schema-name="Contact.CreatedBy">
    <name locale="en-GB">
     Created By
    </name>
   </field>
   <field data-type="DateTime" schema-name="Contact.CreatedTime">
    <name locale="en-GB">
     Created Time
    </name>
   </field>
   <field data-type="SystemAllocation" schema-name="Contact.LastModifiedBy">
    <name locale="en-GB">
     Last Modified By
    </name>
   </field>
   <field data-type="DateTime" schema-name="Contact.LastModifiedTime">
    <name locale="en-GB">
     Last Modified Time
    </name>
   </field>
   <field data-type="ShortText" schema-name="Contact.ParentDisplayName">
    <name locale="en-GB">
     Parent Display Name
    </name>
   </field>
   <field data-type="ShortText" schema-name="Contact.Address01">
    <name locale="en-GB">
     Address Line 1
    </name>
   </field>
   <field data-type="ShortText" schema-name="Contact.Address02">
    <name locale="en-GB">
     Address Line 2
    </name>
   </field>
   <field data-type="ShortText" schema-name="Contact.Address03">
    <name locale="en-GB">
     Address Line 3
    </name>
   </field>
   <field data-type="ShortText" schema-name="Contact.Address04">
    <name locale="en-GB">
     Address Line 4
    </name>
   </field>
   <field data-type="Category" schema-name="Contact.Clientis">
    <name locale="en-GB">
     Client is
    </name>
   </field>
   <field data-type="Category" schema-name="Contact.ContactIs">
    <name locale="en-GB">
     Contact Is
    </name>
   </field>
   <field data-type="ShortText" schema-name="Contact.Mobile">
    <name locale="en-GB">
     Contact Number
    </name>
   </field>
   <field data-type="Category" schema-name="Contact.ContactType">
    <name locale="en-GB">
     Contact Type
    </name>
   </field>
   <field data-type="ShortText" schema-name="Contact.County">
    <name locale="en-GB">
     County
    </name>
   </field>
   <field data-type="DateTime" schema-name="Contact.DateofBirth">
    <name locale="en-GB">
     Date of Birth
    </name>
   </field>
   <field data-type="ShortText" schema-name="Contact.Email">
    <name locale="en-GB">
     E-mail Address
    </name>
   </field>
   <field data-type="ShortText" schema-name="Contact.FirstName">
    <name locale="en-GB">
     First Name
    </name>
   </field>
   <field data-type="ShortText" schema-name="Contact.HomePhone">
    <name locale="en-GB">
     Home Phone
    </name>
   </field>
   <field data-type="ShortText" schema-name="Contact.Organisation">
    <name locale="en-GB">
     Organisation
    </name>
   </field>
   <field data-type="ShortText" schema-name="Contact.Phone01">
    <name locale="en-GB">
     Phone Number 1
    </name>
   </field>
   <field data-type="ShortText" schema-name="Contact.ZipCode">
    <name locale="en-GB">
     Postcode
    </name>
   </field>
   <field data-type="Category" schema-name="Contact.PreferredContactMethod">
    <name locale="en-GB">
     Preferred Contact Method
    </name>
   </field>
   <field data-type="Category" schema-name="Contact.PreferredContactTime">
    <name locale="en-GB">
     Preferred Contact Time
    </name>
   </field>
   <field data-type="DateTime" schema-name="Contact.ReceiptDate">
    <name locale="en-GB">
     Receipt Date
    </name>
   </field>
   <field data-type="ShortText" schema-name="Contact.Reference">
    <name locale="en-GB">
     Reference
    </name>
   </field>
   <field data-type="ShortText" schema-name="Contact.Surname">
    <name locale="en-GB">
     Surname
    </name>
   </field>
   <field data-type="Category" schema-name="Contact.Title">
    <name locale="en-GB">
     Title (Pre April 2020)
    </name>
   </field>
   <field data-type="ShortText" schema-name="Contact.Town">
    <name locale="en-GB">
     Town
    </name>
   </field>
   <field data-type="Journal" schema-name="Case.ActionTaken">
    <name locale="en-GB">
     Action Taken - Old
    </name>
   </field>
   <field data-type="LongText" schema-name="Case.AdditionalComments">
    <name locale="en-GB">
     Additional Comments
    </name>
   </field>
   <field data-type="LongText" schema-name="Case.Description">
    <name locale="en-GB">
     Description
    </name>
   </field>
   <field data-type="LongText" schema-name="Case.ActionTaken01">
    <name locale="en-GB">
     Desired outcome(s)
    </name>
   </field>
   <field data-type="Category" schema-name="Case.Ward">
    <name locale="en-GB">
     Electoral Division
    </name>
   </field>
   <field data-type="Category" schema-name="Case.FeedbackType">
    <name locale="en-GB">
     Feedback Type
    </name>
   </field>
   <field data-type="Category" schema-name="Case.HowReceived">
    <name locale="en-GB">
     How Received
    </name>
   </field>
   <field data-type="DateTime" schema-name="Case.IncidentDate">
    <name locale="en-GB">
     Incident Date
    </name>
   </field>
   <field data-type="Category" schema-name="Case.LearningIdentified">
    <name locale="en-GB">
     Learning Identified?
    </name>
   </field>
   <field data-type="Category" schema-name="Case.OverallOutcome">
    <name locale="en-GB">
     Overall Outcome
    </name>
   </field>
   <field data-type="Category" schema-name="Case.ReceivedinStage">
    <name locale="en-GB">
     Received in Stage
    </name>
   </field>
   <field data-type="Category" schema-name="Case.ServiceAreaTeam">
    <name locale="en-GB">
     Service Director
    </name>
   </field>
   <field data-type="Category" schema-name="Case.Team">
    <name locale="en-GB">
     Team
    </name>
   </field>
   <field data-type="LongText" schema-name="Case.Actions">
    <name locale="en-GB">
     Corporate Actions
    </name>
   </field>
   <field data-type="Category" schema-name="Case.Outcome">
    <name locale="en-GB">
     Corporate Outcome
    </name>
   </field>
   <field data-type="Category" schema-name="Case.Investigator">
    <name locale="en-GB">
     Investigator
    </name>
   </field>
   <field data-type="ShortText" schema-name="Contact.OtherTitle">
    <name locale="en-GB">
     Title
    </name>
   </field>
  </fields>
 </webservice>
        """
    )
    return BeautifulSoup(xml, "xml")
